---
layout: post
title: "Iowa Housing: Cleaning House"
date: 2021-03-17
tags: [python, data exploration, data cleaning, machine learning, iowa housing]
---

In my last post about the Iowa housing data set, I spent some time working with a specific logical flow for filling categorical NA values - you can find that post <a href="/blog/2020/11/11/filling-NA-values">here</a>.
In the post previous to that, I visualized some features, using a lot of box / violin plots, count plots, and some linear regression scatter plots comparing the distribution of SalePrices when sorted by specific features. If you would like a refresher, check that post out <a href="/blog/2020/08/05/iowa-housing-exploration">here</a>.

In this post, I'm going to walk through my process of cleaning the data in order to retain as much information as possible. Thanks to Kaggle users <a href="https://www.kaggle.com/datafan07">Ertuğrul Demir</a> and <a href="https://www.kaggle.com/goldens">Golden</a> for posting their in-depth notebooks. Both contain a wealth of information and provide a great starting base for other novice data analysts.

<br>

___

### Examining the Missing Data ###

By now, I'm quite familiar with this data set - but it won't hurt us to generate a table of values specifically to highlight our missing data!

The first thing I want to do is examine the null / <code>NA</code> values in both of the train and test datasets. To do this, we'll have three datasets: <code>train_data</code>, <code>test_data</code>, and <code>merged_data</code>. The <code>merged_data</code> dataset has all of our samples from both of the train and test datasets without the <code>SalePrice</code> feature, which will make it easier for us to look at the aggregated data.

{% highlight python %}
# create features dataframes,
# dropping SalePrice from
# train_features
train_features =
  train_data.drop(
    ['SalePrice'],
     axis=1)
test_features =
  test_data

# merge the two data sets
# for analysis, and reset index
merged_data = pd.concat(
  [train_features,
   test_features]).reset_index(
    drop=True)

datasets = [train_data,
  test_data,
  merged_data]
{% endhighlight %}

Having an array of datasets will come in handy later when we need to access each dataset to make any adjustments.

Using <code>merged_data</code>, I created a summary table with three purposes:

(1) Calculate how many samples have <code>NA</code>s for each feature,

(2) Describe the data type of each feature,

(3) Give a list of unique values for each categorical feature, and a min / max / mean / median summary for each numerical feature.

This is easily visualized in the table below:

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th class='text'>Feature</th>
      <th class='numeric'>NA Count</th>
      <th class='numeric'>% Missing</th>
      <th class='text'>Data Type</th>
      <th class='text'>Overview</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th data-title='Feature' class='text'>PoolQC</th>
      <td data-title='NA Count' class='numeric'>2909</td>
      <td data-title='% Missing' class='numeric'>0.99657</td>
      <td data-title='Data Type' class='text'>object</td>
      <td data-title='Overview' class='text'>[nan, Ex, Fa, Gd]</td>
    </tr>
    <tr>
      <th data-title='Feature' class='text'>MiscFeature</th>
      <td data-title='NA Count' class='numeric'>2814</td>
      <td data-title='% Missing' class='numeric'>0.96403</td>
      <td data-title='Data Type' class='text'>object</td>
      <td data-title='Overview' class='text'>[nan, Shed, Gar2, Othr, TenC]</td>
    </tr>
    <tr>
      <th data-title='Feature' class='text'>Alley</th>
      <td data-title='NA Count' class='numeric'>2721</td>
      <td data-title='% Missing' class='numeric'>0.93217</td>
      <td data-title='Data Type' class='text'>object</td>
      <td data-title='Overview' class='text'>[nan, Grvl, Pave]</td>
    </tr>
    <tr>
      <th data-title='Feature' class='text'>Fence</th> 
      <td data-title='NA Count' class='numeric'>2348</td>
      <td data-title='% Missing' class='numeric'>0.80439</td>
      <td data-title='Data Type' class='text'>object</td>
      <td data-title='Overview' class='text'>[nan, MnPrv, GdWo, GdPrv, MnWw]</td>
    </tr>
    <tr>
      <th data-title='Feature' class='text'>FireplaceQu</th>
      <td data-title='NA Count' class='numeric'>1420</td>
      <td data-title='% Missing' class='numeric'>0.48647</td>
      <td data-title='Data Type' class='text'>object</td>
      <td data-title='Overview' class='text'>[nan, TA, Gd, Fa, Ex, Po]</td>
    </tr>
    <tr>
      <th data-title='Feature' class='text'>LotFrontage</th>
      <td data-title='NA Count' class='numeric'>486</td>
      <td data-title='% Missing' class='numeric'>0.16650</td>
      <td data-title='Data Type' class='text'>float64</td>
      <td data-title='Overview' class='text'>[21, 313, 69.0, 68]</td>
    </tr>
    <tr>
      <th class='styling-space'>...</th>
      <td class='styling-space' class='disappearing'>...</td>
      <td class='styling-space' class='disappearing'>...</td>
      <td class='styling-space' class='disappearing'>...</td>
      <td class='styling-space' class='disappearing'>...</td>
    </tr>
  </tbody>
</table>

<a class='read-more-link' href='/assets/missing-values-summary.html'> See full table </a>

<center>The script that generated this table is available on <a href="https://github.com/aimosjo/aimee.codes/blob/main/assets/code/missingValuesSummary.py">my github</a>.</center>

We've got our work laid out, time to start cleaning!
<br>

___


### Filling the Missing Data ###

#### Categorical Features with "NA / nan" which mean "None" ####

For many of the categorical features, <code>NA</code> is used if the sample doesn't contain the given feature. For these samples, we will change the sample feature to <code>None</code> instead. 

{% highlight python %}none_cols = [
  'PoolQC',
  'MiscFeature',
  'Alley',
  'Fence',
  'FireplaceQu',
  'GarageFinish',
  'GarageQual',
  'GarageCond',
  'GarageType',
  'BsmtCond',
  'BsmtExposure',
  'BsmtQual',
  'BsmtFinType1',
  'BsmtFinType2',
  'MasVnrType'
]

for col in none_cols:
  for ds in datasets:
      ds[col] = 
        ds[col].fillna("None")
{% endhighlight %}
<br>
<hr width="40%" />
<br>
#### Numerical features with "NA / nan" which mean 0 ####

These numerical features just need 0 instead of <code>NA</code>, since for these samples, the feature doesn't exist.

{% highlight python %}
zero_cols = [
  'GarageYrBlt',
  'MasVnrArea',
  'BsmtFullBath',
  'BsmtHalfBath',
  'BsmtFinSF1',
  'BsmtFinSF2',
  'BsmtUnfSF',
  'TotalBsmtSF']

for col in zero_cols:
  for ds in datasets:
      ds[col] =
        ds[col].fillna(
        0, inplace=True)
{% endhighlight %}

<br>
<hr width="40%" />
<br>
#### Categorical features with "NA / nan" which need examination ####

These are categorical features which are missing from 1-4 samples.

#### MSZoning / Exterior1st / Exterior2nd ####

*Filling <code>MSZoning</code> is the subject of another post, which can be found <a href="/blog/2020/11/11/filling-NA-values">here</a>!*

Since the distribution of values for <code>MSZoning</code>, <code>Exterior1st</code>, and <code>Exterior2nd</code> appear to depend on which <code>Neighborhood</code> the house is located in, we need to group our features by <code>Neighborhood</code>, then use the mode of the given feature to fill in the NAs.

There is only 1 sample that is missing both Exterior1st and Exterior2nd features, and it is in the Edwards <code>Neighborhood</code>: 
{% highlight python %}
mask1 = merged_data[ 
  'Exterior1st'].isna()
mask2 = merged_data[ 
  'Exterior2nd'].isna()
merged_data[mask1 & mask2]
  ['ExterQual',
  'ExterCond',
  'Neighborhood']

      EQ  EC  Neighborhood
2151  TA   3  Edwards
{% endhighlight %}

To make an accurate prediction, we can examine other houses in the Edwards <code>Neighborhood</code> with identical <code>ExterQual</code> and <code>ExterCond</code> values to see what the distribution looks like:

{% highlight python %}
mask3 = merged_data[
  'Neighborhood'] == 'Edwards'
mask4 = merged_data[
  'ExterQual'] == 'TA'
mask5 = merged_data[
  'ExterCond'] == 'TA'

merged_data[mask3
  & mask4 & mask5][[
  'Exterior1st',
  'Exterior2nd']].value_counts()

Exterior1st  Exterior2nd
Wd Sdng      Wd Sdng        36
MetalSd      MetalSd        28
VinylSd      VinylSd        22
Plywood      Plywood        12
HdBoard      HdBoard         9
WdShing      Wd Shng         9
HdBoard      Plywood         5
Stucco       Stucco          4
WdShing      Plywood         4
BrkFace      Wd Sdng         3
AsbShng      Plywood         2
             AsbShng         2
Plywood      Wd Shng         1
VinylSd      Wd Sdng         1
MetalSd      Wd Sdng         1
             HdBoard         1
Wd Sdng      Plywood         1
BrkFace      Plywood         1
BrkComm      Brk Cmn         1
AsphShn      AsphShn         1
{% endhighlight %}

From the above result, we should be able to see Wd Sdng is the most common <code>Exterior1st</code> and <code>Exterior2nd</code> value for homes in the Edwards <code>Neighborhood</code> with TA for both <code>ExterQual</code> and <code>ExterCond</code> values. This is the value we want assigned to both <code>Exterior1st</code> and <code>Exterior2nd</code> for the missing value.

{% highlight python %}
nbh_mode_list = ['MSZoning',
  'Exterior1st',
  'Exterior2nd']

for ds in datasets:
  for col in nbh_mode_list:
    ds[col] =
      ds[col].fillna(
      ds.groupby('Neighborhood')
      [col].transform(
      lambda x:
        x.mode().iloc[0]))
{% endhighlight %}

#### Functional ####

It appears <code>Functional</code> measures how many safety deductions the house has / how much overall damage there is. I started this investigation by examining 4 features: <code>OverallCond</code>, <code>BsmtCond</code>, <code>ExterCond</code>, and <code>GarageCond</code>. These features could give us an idea of any damage to the home, and if <code>Functional</code> is affected.

{% highlight python %}
condFeatures = [
  'OverallCond',
  'BsmtCond',
  'ExterCond',
  'GarageCond']
{% endhighlight %}

First, only 2 samples from the test set are missing this feature: 

{% highlight python %}

mask4 = merged_data[
'Functional'].isna()

merged_data[mask4][
  ['Id',
   'Functional'] +
  condFeatures]

Id     Func  OvC BC   EC  GC
2217   NaN    5  None Po  Po
2474   NaN    1  Fa   Fa  Fa
{% endhighlight %}

Something a little funky to notice here: While house with <code>Id</code> 2217 has no basement, poor exterior condition, and poor garage condition, it still has an overall condition score of 5, while house with <code>Id</code> 2474 has a fair basement, fair exterior condition, and fair garage condition still only has an overall condition rating of 1. This doesn't really make sense under my hypothesis of a higher condition rating correlating with a higher functionality rating, so we had better keep investigating. 

We need to get the data looking like something we can numerically manipulate. This will take two steps:

  (1) Pop out all of these features into a separate deep copied dataframe so none of my fiddling will affect the underlying data.
{% highlight python %}
mask5 = merged_data['Functional'].isna()
condfeatdf = merged_data[~mask5][
  ['Id',
   'Functionality',
   condFeatures]].copy(deep=True)

Id   Func  OC 	BC   EC   GC
1    Typ   5 	TA   TA   TA
2    Typ   8 	TA   TA   TA
3    Typ   5 	TA   TA   TA
4    Typ   5 	Gd   TA   TA
5    Typ   5 	TA   TA   TA
...  ...   ... 	...  ...  ...
{% endhighlight  %}

  (2) Encode these variables as integers instead of categorical variables despite my lingering doubts about the linearity of the condition scale (we don't know the exact differences between a 'Po' house and a 'Fa' house) so we can actually perform a correlation test between all of the selected features. 

{% highlight python %}
cond_map = {
  'None': 0,
  'Po': 1,
  'Fa': 2,
  'TA': 3,
  'Gd': 4,
  'Ex': 5
}
func_map = {
  'Sal': 0,
  'Sev': 1,
  'Maj2': 2,
  'Maj1': 3,
  'Mod': 4,
  'Min2': 5,
  'Min1': 6,
  'Typ': 7
}

for feat in condFeatures[1:]:
  condfeatdf[feat] =
    condfeatdf[feat].map(
     cond_map).astype('int')
condfeatdf['Functional'] =
  condfeatdf['Functional'].map(
    func_map).astype('int')

Id  Func  OC  BC  EC  GC
1   7 	  5   3   3   3
2   7 	  8   3   3   3
3   7     5   3   3   3
4   7     5   4   3   3
5   7     5   3   3   3
{% endhighlight %}

That looks better! Now we can attempt some numerical manipulations:

{% highlight python %}
condfeatdf.corr()[1:][
  ['Functional',
   'OverallCond',
   'BsmtCond',
   'ExterCond',
   'GarageCond']]

     OC     BC     EC     GC
Func 0.118  0.190  0.074  0.090
OC          0.090  0.403  0.045
BC                 0.096  0.140
EC                        0.093
{% endhighlight %}

This doesn't bode well for my hypothesis at all - if we consider the condition scales linear, then the feature with the highest correlation to <code>Functional</code> is <code>BsmtCond</code> with a value of only 0.19.

Another issue is that many homes have a <code>BsmtCond</code> value of 0 under the new mapping, and it is not immediately clear that if a house has a <code>BsmtCond</code> of 0, it does not have a lower quality basement than a home with a <code>BsmtCond</code> value of 1. There are a lot of assumptions here, and frankly for only 2 missing values, this entire expedition may have been overkill. Ultimately, we will fill the two <code>NA</code> values with the mode, and fondly remember how to use <code>map</code> for the next time we need to change from a categorical variable to a numerical one. Good thing I made a deep copy to play around with instead!

{% highlight python %}
for ds in datasets:
  ds['Functional'] =
    ds['Functional'].fillna(
    ds['Functional'].mode()[0])
{% endhighlight %}

#### Electrical / KitchenQual / SaleType / Utilities ####

For these variables, there's only 1-2 samples missing each feature, so we will fill them with the mode of the feature from the dataset.

{% highlight python %}
for col in (
  'Electrical',
  'KitchenQual',
  'SaleType',
  'Utilities'):
    for ds in datasets:
      ds[col] = ds[col].fillna(
        ds[col].mode()[0]
{% endhighlight %}

<br>
<hr width="40%" />
<br>
#### Numerical features with "NA / nan" which need examination ####

There's a little more happening here than what appears at surface level, so let's take a deeper dive into these features: 

#### LotFrontage ####

This is one of the features which a significant number of samples (486 / 2919) are missing. Lot frontage is defined as "linear feet of street connected to property." Certainly we can draw the conclusion that <code>LotArea</code> might be correlated to <code>LotFrontage</code> since one is used to calculate the other, but there are a few other features that can help us interpolate.

First, let's see the correlation between <code>LotArea</code> and <code>LotFrontage</code>.

{% highlight python %}
merged_data[
  ['LotArea', \
  'LotFrontage']].corr()

    LotArea   LotFrontage
LA  1.000000  0.489896
LF  0.489896  1.000000
{% endhighlight %}

0.48 isn't a very strong correlation value - there isn't a clear linear relationship between our two features. However, we're going to examine another feature <code>LotConfig</code> which can tell us more about the relationship of <code>LotFrontage</code> and <code>LotArea</code>. 

{% highlight text %}
LotConfig:  Lot configuration
  Inside    Inside lot
  Corner    Corner lot
  CulDSac   Cul-de-sac
  FR2       Frontage on 2 sides
            of property
  FR3       Frontage on 3 sides
            of property
{% endhighlight %}

Considering how <code>Corner</code> lots may have twice as much <code>LotFrontage</code> as <code>Inside</code> lots, and <code>FR2</code>s and <code>FR3</code>s should have comparatively more as well, first sorting into <code>LotConfig</code> might help us calculate a more accurate prediction.

First, we can examine the distribution of the <code>LotConfig</code> feature of the samples which are missing <code>LotFrontage</code>:

{% highlight python %}
mask6 = merged_data['LotFrontage'].isna()
merged_data[mask6]
  ['LotConfig'].value_counts()

Inside     271
Corner     104
CulDSac     87
FR2         20
FR3          4
{% endhighlight %}

~77% (374/486) of our samples with a missing <code></code> value have either Inside or Corner as a <code>LotConfig</code>. To get a better idea of the correlation between these variables, we can look at how a simple linear model lines up on the subplots of each configuration:

<section id='photos-grid'>
  <img src="/assets/images/AreaFrontageSubplot0.svg" width='98%'>
  <img src="/assets/images/AreaFrontageSubplot1.svg" width='98%'>
  <img src="/assets/images/AreaFrontageSubplot2.svg" width='98%'>
  <img src="/assets/images/AreaFrontageSubplot3.svg" width='98%'>
  <img src="/assets/images/AreaFrontageSubplot4.svg" width='98%'>
</section>

<center>The code used to generate these graphs is available <a href="https://github.com/aimosjo/aimee.codes/blob/main/assets/code/featureEngineeringGraphs.py">on my github</a>.</center>

Important to notice - I limited the <code>LotArea <= 80000</code> since there is one outlier which skews all figures off to the right, at over 200000 square feet (200 when scaled, as seen here).

You can also see there is an issue with <code>CulDSac</code> properties - the linear model does not fit the data at all. Below, you can see this reflected in the correlations between <code>LotArea</code> and <code>LotFrontage</code> when grouped by <code>LotConfig</code>.

{% highlight python %}
mask6 = merged_data[
  'LotArea'] <= 80000
merged_data[mask6].groupby(
  'LotConfig')[
    ['LotArea',
    'LotFrontage']].corr()

              LA        LF
LotConfig
Inside    LA  1.000000  0.630001
          LF  0.630001  1.000000
Corner    LA  1.000000  0.787955
          LF  0.787955  1.000000
CulDSac   LA  1.000000  0.195327
          LF  0.195327  1.000000
FR2       LA  1.000000  0.827626
          LF  0.827626  1.000000
FR3       LA  1.000000  0.835891
          LF  0.835891  1.000000
{% endhighlight %}

Comparing this to our previous correlation calculation, there is a strict improvement in correlation for all <code>LotConfig</code> features except for <code>CulDSac</code> which could be due to the irregular shape of <code>CulDSac</code> lots, and their disproportionately small <code>LotFrontage</code> measure. I predict that, even with the poor predictions for <code>CulDSac</code> lots which make up 87 of our missing 486, we will have success using the linear relationship between <code>LotArea</code> and <code>LotFrontage</code> grouped by <code>LotConfig</code> to fill in our missing <code>LotFrontage</code> feature.

To do this, I will separate <code>merged_data</code> into 5 subsets (one for each possible value of <code>LotConfig</code>), remove the <code>NA</code>s from each subset, and then use the resulting subset to train a linear model.

The code used to do this is much easier to view <a href="">on github</a>, since I used a custom function, which, when applied to the data, is able to replace an <code>NA</code> <code>LotFrontage</code> value with a predicted one.

To see how this affected our data, we can compare the previous graphs to updated ones - we should be able to see new data points running along our previously displayed line of best fit for each <code>LotConfig</code>.

<section id="photos-two">
  <img src="/assets/images/AreaFrontageSubplot0.svg" width = "49%">
  <img src="/assets/images/AreaFrontageSubplotPostFill0.svg" width="49%">
</section>

<section id="photos-two">
  <img src="/assets/images/AreaFrontageSubplot1.svg" width = "49%">
  <img src="/assets/images/AreaFrontageSubplotPostFill1.svg" width="49%">
</section>
<section id="photos-two">
  <img src="/assets/images/AreaFrontageSubplot2.svg" width = "49%">
  <img src="/assets/images/AreaFrontageSubplotPostFill2.svg" width="49%">
</section>
<section id="photos-two">
  <img src="/assets/images/AreaFrontageSubplot3.svg" width = "49%">
  <img src="/assets/images/AreaFrontageSubplotPostFill3.svg" width="49%">
</section>
<section id="photos-two">
  <img src="/assets/images/AreaFrontageSubplot4.svg" width = "49%">
  <img src="/assets/images/AreaFrontageSubplotPostFill4.svg" width="49%">
</section>

It is not perfect, but it does let us keep <code>LotFrontage</code> as a feature, and this might help boost the performance of our algorithm. Another way we can visualize how the data was changed is by using <code>.describe()</code> on <code>merged_data['LotFrontage']</code> before and after filling.

{% highlight python %}
         Prefill  Postfill 
count    2433.00   2919.00    
mean       69.30     70.17
std        23.34     27.03
min        21.00     21.00
25%        59.00     58.32
50%        68.00     68.00
75%        80.00     80.00
max       313.00    806.26
{% endhighlight %}

#### GarageArea / GarageCars ####

First, we should confirm that the single sample that is missing both <code>GarageArea</code> and <code>GarageCars</code> has a <code>GarageType</code> other than <code>None</code>, otherwise we will simply fill these in with <code>0</code>.

{% highlight python %}
merged_data[
 merged_data[
  'GarageCars'].isna()][[
   'GarageType',
   'GarageArea',
   'GarageCars']]

         GType  GArea  GCars
2576    Detchd    NaN    NaN
{% endhighlight %}

Now, we can fill these based on the average <code>GarageArea</code> of <code>Detchd</code> garages, and the most common value for <code>GarageCars</code> of <code>Detchd</code> garages.

{% highlight python %}
for ds in (
  test_data,
  train_data,
  merged_data):
    ds['GarageCars'] = \
      ds['GarageCars'].fillna(
      groupby('GarageType') \
      ['GarageCars'].transform(
      lambda x: x.mode().iloc[0]))
    ds['GarageArea'] = \
      ds['GarageArea'].fillna(
      groupby('GarageType') \
      ['GarageArea'].transform(
      lambda x: x.mean().iloc[0]))
{% endhighlight %}

<br>

___

### Reviewing the Cleaned Data ###

We can now run the same script to generate our summary of the data - we should see there are no more <code>NA</code> values!

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th class='text'>Feature</th>
      <th class='numeric'>NA Count</th>
      <th class='numeric'>Percentage</th>
      <th class='text'>Data Type</th>
      <th class='text'>Overview</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th data-title='Feature' class='text'>Id</th>
      <td data-title='NA Count' class='numeric'>0</td>
      <td data-title='% Missing' class='numeric'>0.0</td>
      <td data-title='Data Type' class='numeric'>int64</td>
      <td data-title='Overview' class='text'>[1, 2919, 1460, 1460]</td>
    </tr>
    <tr>
      <th data-title='Feature' class='text'>MSSubClass</th>
      <td data-title='NA Count' class='numeric'>0</td>
      <td data-title='% Missing' class='numeric'>0.0</td>
      <td data-title='Data Type' class='numeric'>int64</td>
      <td data-title='Overview' class='text'>[20, 190, 57, 50]</td>
    </tr>
    <tr>
      <th data-title='Feature' class='text'>MSZoning</th>
      <td data-title='NA Count' class='numeric'>0</td>
      <td data-title='% Missing' class='numeric'>0.0</td>
      <td data-title='Data Type' class='text'>object</td>
      <td data-title='Overview' class='text'>[RL, RM, C (all), FV, RH]</td>
    </tr>
    <tr>
      <th data-title='Feature' class='text'>LotFrontage</th>
      <td data-title='NA Count' class='numeric'>0</td>
      <td data-title='% Missing' class='numeric'>0.0</td>
      <td data-title='Data Type' class='numeric'>float64</td>
      <td data-title='Overview' class='text'>[21, 806, 70, 68]</td>
    </tr>
    <tr>
      <th class='styling-space'>...</th>
      <td class='styling-space' class='disappearing'>...</td>
      <td class='styling-space' class='disappearing'>...</td>
      <td class='styling-space' class='disappearing'>...</td>
      <td class='styling-space' class='disappearing'>...</td>
    </tr>
  </tbody>
</table>

<a class='read-more-link' href='/assets/cleaned-missing-values-summary.html'> See full table </a>

No more NAs!!

This has been a beast of a post, both in length and content! Now that we have a squeaky clean dataset, the next step will be some feature engineering, and possibly some exploration into feature selection using a Random Forest Regressor. 

Thank you for reading, until next time!