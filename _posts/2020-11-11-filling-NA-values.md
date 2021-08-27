---
layout: post
title: "Filling Categorical NAs"
date: 2020-11-11
tags: [python, pandas, data exploration, data cleaning, iowa housing, optimization]
---

<zw>好久不见了！</zw>Long time, no see! In my last post, I gave a long update of tasks I took on after moving my little family to a new apartment in a new city. Now that we have settled into the new place and my language classes have become a familiar process, I\'ve gotten back into the data science swing and returned to the Iowa housing data set. 

[If you want to see my work so far on this dataset, click the tags above and you can see all related posts.]

Now, as I have been working with this dataset, I\'ve run into an interesting problem that I wanted to dedicate a blog post to: filling an NA value with the mode of a series based on a single feature\'s row value (yikes!). To illustrate this, let\'s get a quick background to the problem: 

Our dataset has some missing values, and I want to create a \"rule\" to fill in the NAs. The feature I am currently concerned with is `MSZoning`, which only 4 samples from our `test_data` set are missing.

From the official dataset description file, we get some clues about what `MSZoning` represents: 

{% highlight python %}
MSZoning: Identifies the general zoning classification of the sale.

  A	Agriculture
  C	Commercial
  FV	Floating Village Residential
  I	Industrial
  RH	Residential High Density
  RL	Residential Low Density
  RP	Residential Low Density Park 
  RM	Residential Medium Density
{% endhighlight %}

Looks like it is general idea of what the property is used for. Now we can go ahead and pull some more information about our properties with missing values out of the dataframe:

{% highlight python %}
test_data[test_data['MSZoning'].isna()][['Id', 'MSZoning', 'Neighborhood', 'MSSubClass']] 

  Id MSZoning Neighborhood  MSSubClass
1916      NaN       IDOTRR          30
2217      NaN       IDOTRR          20
2251      NaN       IDOTRR          70
2905      NaN      Mitchel          20

{% endhighlight %}

I have some options: first, I could simply fill in the NAs by hand (there are only 4 of them). This way, I have complete control over the values, and I can use whatever logic I want in order to fill them.

Secondly, I could write a rule for the pandas `fillna` function. This is by far the more interesting approach, since it allows for scalability and application of `groupby`, `agg`, `apply`, and `transform` functions. My difficulty here (and what this post will focus on) is how to pass my desired logic into the `fillna` function. 

To begin, it is worthwhile looking at the by-hand method to understand what we're trying to accomplish here.

___

**Option 1: By-Hand**

The first thing I want to draw attention to is the most common `MSZoning` variable. We can check the mode of both datasets, and get a quick summary:

{% highlight python %}
train_data['MSZoning'].value_counts()
RL         1151
RM          218
FV           65
RH           16
C (all)      10

test_data['MSZoning'].value_counts()
RL         1114
RM          242
FV           74
C (all)      15
RH           10
{% endhighlight %}

So, the two datasets definitely share a mode: `RL`. However, if we divide our dataset into neighborhoods and then count up each `MSZoning` value, we see a new trend emerge: 

<section id='photos'>
  <img src="/assets/images/2020-11-11/ZoneCountPlot.svg" width='98%'>
</section>
(Note that only 8 of 25 neighborhoods are included here for ease of viewing, you can see the full figure with all 25 neighborhoods <a href="/assets/zone-plot-full.html">here</a>)

My biggest take-aways from this graphic:

<ol>
  <li>Each neighborhood only has 1-3 unique `MSZoning` values.</li>
  <li>Some neighborhoods do not share the overall mode of the dataset!</li>
</ol>

For example, in the Somerset Neighborhood the mode is actually `FV` or Floating Village Residential, and in the IDOTRR (Iowa Department of Transport and Rail Road) Neighborhood the mode is `RM`, or Residential Medium Density. Since 3 of our 4 homes are in the IDOTRR Neighborhood, we should be careful about filling NAs with the mode of the overall dataset.

The easiest thing is to hand-fill the NAs based on the <i>mode</i> of the subset of the Neighborhood. This is pretty simple, and the only snag we hit is dealing with indices (non-trivial!) if we merged our datasets, or adjusted their positions in anyway.

Thus, for the 3 properties without `MSZoning` in IDOTRR, we will replace the NA with `RM`, and the property in Mitchel will be replaced with `RL`. 

{% highlight python %}
test_data.at[455, 'MSZoning'] = 'RM'
test_data.at[756, 'MSZoning'] = 'RM'
test_data.at[790, 'MSZoning'] = 'RM'
test_data.at[1444, 'MSZoning'] = 'RL'
{% endhighlight %}

Again, note here that I had to find the indices and access each value by hand. This is fine for a small number of fixes, but I need a way to automate this process so I can reuse the logical structure in a larger setting!

___

**Option 2: Automation**

My general idea here is to pass the same kind of hand-checked logic to the `fillna` function: if this sample has an NA for `MSZoning`, calculate the most common `MSZoning` value for all homes with the sample\'s Neighborhood value, and then assign the most common value.

While researching how I could attempt this, I found <a href="https://stackoverflow.com/a/51117932">this</a> answer on stackoverflow; this gave me some great insight into using the pandas function `groupby`, and how I could adapt it to my problem. First, let\'s see what groupby does if I decide I want to group `train_data` by *Neighborhood*, and then see the *mean* SalePrice, followed by the *standard deviation* of our SalePrice feature: 

{% highlight python %}
# initialize the Series as a DataFrame column
neigh_saleprice_sum = pd.DataFrame(grouped['SalePrice'].mean())

# add standard deviation as column to dataframe
neigh_saleprice_sum['StdDev'] = grouped['SalePrice'].std()

# round columns to 2 decimal places
neigh_saleprice_sum['MeanSalePrice'] = pd.Series([round(val,2) for val in neigh_saleprice_sum['MeanSalePrice']], index = neigh_saleprice_sum.index)

neigh_saleprice_sum['StdDev'] = pd.Series([round(val,2) for val in neigh_saleprice_sum['StdDev']], index = neigh_saleprice_sum.index)

neigh_saleprice_sum

              MeanSalePrice     StdDev
Neighborhood                          
Blmngtn           194870.88   30393.23
Blueste           137500.00   19091.88
BrDale            104493.75   14330.18
BrkSide           124834.05   40348.69
ClearCr           212565.43   50231.54
CollgCr           197965.77   51403.67
Crawfor           210624.73   68866.40
Edwards           128219.70   43208.62
Gilbert           192854.51   35986.78
IDOTRR            100123.78   33376.71
MeadowV            98576.47   23491.05
Mitchel           156270.12   36486.63
NAmes             145847.08   33075.35
NPkVill           142694.44    9377.31
NWAmes            189050.07   37172.22
NoRidge           335295.32  121412.66
NridgHt           316270.62   96392.54
OldTown           128225.30   52650.58
SWISU             142591.36   32622.92
Sawyer            136793.14   22345.13
SawyerW           186555.80   55652.00
Somerst           225379.84   56177.56
StoneBr           310499.00  112969.68
Timber            242247.45   64845.65
Veenker           238772.73   72369.32
{% endhighlight %}

Awesome - we created a customized summary of SalePrice for each Neighborhood. We could do this kind of summary for any numerical feature in our dataset, grouped specifically by a selected categorical feature.

Now, if we wanted to, we could initialize a SalePrice variable in our test_data set, assign the mean SalePrice of the neighborhood to each test_data sample, and call it a day! Machine Learning™ Completed. I don't think we'd get fantastic accuracy though, considering the second column above, so we'd better keep searching for a better method.

One issue is that there is not a `.mode()` we can use at the end of our statement - this groupby function only works with numerical summaries, like mean, variance, or median. So we need to find a work-around, since our data is categorical and we're assigning it based on the Neighborhood\'s mode.

{% highlight python %}
grouped['SalePrice'].mode()

AttributeError: 'SeriesGroupBy' object has no attribute 'mode'
{% endhighlight %}

Thankfully, I found <a href="https://stackoverflow.com/a/59127538">another</a> potential answer. This one suggested bringing `transform`, `agg`, and `apply` into the mix. A great primer for understanding how these function works can be found <a href="https://pbpython.com/pandas_transform.html">here</a>. 

I found that when I used `transform`, it had the same limitations as earlier - I couldn't use it on categorical variables immediately. However, I found when I used `agg`, I was able to get some great results! Below, we are going to find the most common value for `MSZoning` sorted by `Neighborhood`.

{% highlight python %}
merge_data.groupby('Neighborhood')['MSZoning'].agg(pd.Series.mode)
Neighborhood
Blmngtn    RL
Blueste    RM
BrDale     RM
BrkSide    RM
ClearCr    RL
CollgCr    RL
Crawfor    RL
Edwards    RL
Gilbert    RL
IDOTRR     RM
MeadowV    RM
Mitchel    RL
NAmes      RL
NPkVill    RL
NWAmes     RL
NoRidge    RL
NridgHt    RL
OldTown    RM
SWISU      RL
Sawyer     RL
SawyerW    RL
Somerst    FV
StoneBr    RL
Timber     RL
Veenker    RL
{% endhighlight %}

This is a great sign - it is returning the most common value of `MSZoning` for each `Neighborhood`! As we saw earlier, the most common `MSZoning` value for the `Neighborhood` of `'Somerset'` is indeed `FV`. Now that we have something that works, I want to walk through my logic before we jump into writing the code that works. 

My first thought: I could simply calculate this variable and assign it as a column for every single sample in our test data, so it is a fast and easy fix to simply assign a missing sample\'s calculated mode as it\'s `MSZoning` value. However, let\'s remember: there are 1459 samples in my `test_data` set. I am not going to waste time creating an additional, useless variable for 1455 samples. This is not great for scalability, and a huge waste of my computer\'s limited processing power. 

Instead, I\'m going to use the pandas `fillna` function, which should have an easier time detecting NAs in our selected column, and doing minor computations to fill.

The function `fillna` can take a function, which will execute when an NA passes in. Let\'s take a look at the code below: 

{% highlight python %}
for ds in (test_data, train_data, merge_data):
	ds['MSZoning'] = ds['MSZoning'].fillna(ds.groupby('Neighborhood')['MSZoning'].transform(lambda x: x.mode().iloc[0]))
{% endhighlight %}

Here, you\'ll notice I have three datasets: these are my training samples which I\'ll train my model on; testing samples which I\'ll use to test the accuracy of my model; and a merged dataset of my test and training data, minus our target variable (`SalePrice`), which I\'m using to fill in and summarize the data. 

As well, you\'ll notice I passed in a lambda function: here, I\'m asking it to assign the mode of the `MSZoning` feature, grouped by `Neighborhood`. After this code runs, we can check to see if any NAs remain in our data sets, and check the assigned variables at our indices: 

{% highlight python %}
# check to make sure no more NAs exist for this variable
for ds in (test_data, train_data, merge_data):
  print(ds[ds['MSZoning'].isna()])

Empty DataFrame

Empty DataFrame

Empty DataFrame

{% endhighlight %}

So far, so good - let\'s see what the values are at our previously NA locations:

{% highlight python %}
test_data.at[455, 'MSZoning']
'RM'

test_data.at[756, 'MSZoning']
'RM'

test_data.at[790, 'MSZoning']
'RM'

test_data.at[1444, 'MSZoning']
'RL'
{% endhighlight %}

Great, it works exactly like it ought to! You can find my full cleaning script posted on my <a href="https://github.com/aimeecodes/aimee.codes/blob/main/assets/code/2020-11-11/iowaprerun.py">github</a>.

___

**Final Results**

Using `groupby`, `transform` and a lambda function, I was able to fill in categorical NAs based on the mode of another categorical variable, by grouping the dataset by *another* categorical variable. This way, I can write two short lines of code into my prerun cleaning script, and get to working with more accurate data. Another variable I\'ll use this kind of prediction on is `Exterior1st / Exterior2nd`, since these features also seem to correlate with `Neighborhood`.

That\'s all for today\'s post, I\'ll have another large update to post when I\'ve finished cleaning my dataset and prepared it for algorithm testing. Until next time, stay safe and wear a mask!
