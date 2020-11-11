---
layout: post
title: "iowa housing exploration"
date: 2020-08-05
tags: [python, data visualization, data exploration, iowa housing]
---
<style>
	.img-container {
	text-align: center;
	}
</style>

My latest project (which I started talking about in my last post here) is related to Kaggle's ML competition to predict housing prices given 81 features of homes in Ames, Iowa. Let's jump back in!

I want to visualize some of the data, and see what relations exists between the features and our target output SalePrice.

After taking a look at the feature descriptions, I'm going to generate a few plots to check out:
* OverallQual - Rates the overall material and finish of the house
* BldgType: Type of dwelling
* HouseStyle: Style of dwelling
* Utilities: Type of utilities available
* GrLivArea - Above grade (ground) living area square feet
* GarageType - Garage location
* GarageArea - Size of garage in square feet
* MoSold - Month Sold
* SaleType - Type of sale (Warranty deed, contract, estate, etc)

For this project, I used Seaborn (a library that works on top of matplotlib) to generate a few quick plots to give me an idea of what my dataset looks like. 

___

<i>EDIT:</i> After exploring the dataset even more during my next phase, I realized I overlooked a key feature: OverallQual. If we sort SalePrice by OverallQual, we see something quite obvious, but nonetheless telling:

<center>
	<img src="/assets/images/2020-08-05/SalePriceOverallQualBox.png" width = "49%">
	<img src="/assets/images/2020-08-05/OverallQualCount.png" width="49%">
</center>

As OverallQual increases, it appears the SalePrice does too - there are more ways of testing this hypothesis, which I'll explore in another blog post. For now, we should take away that our dataset mostly consists of homes rated between 4-8 inclusive, with a slightly right skewed distribution.

___

Next up, I wanted to explore how SalePrice and BldgType were related. I created these plots to see the spread of SalePrice when separated into BldgTypes, and see the count for each BldgType in our dataset.

<center>
	<img src="/assets/images/2020-08-05/BuildingTypeSalePriceBoxen.png" width="49%"> 
	<img src="/assets/images/2020-08-05/BldgTypeCount.png" width="49%"> 
</center>
(thank you to <a href="https://stackoverflow.com/questions/49044131/how-to-add-data-labels-to-seaborn-countplot-factorplot/49052124">this</a> poster for helping me out with the labels on the second plot!)

As you can see, there's an overwhelming number of Single-family Detatched homes for our algorithm to train on, but not a lot of other types - as well, the spread of SalePrice pretty large for all BldgTypes. Hopefully there are other features that will help divy up the Single-family Detatched category!

___

Here are some more graphs I generated from the data - there are interesting things happening with GarageArea, GarageType, and SalePrice:

<center>
	<img src="/assets/images/2020-08-05/GarageSalePrice.png" width="60%"> 
</center>

It appears that the price of each GarageType scales differently according to GarageArea. This could be very useful for our algorithm to pick up on! (This may also be explained by the relation of the GarageType being associated with different HouseStyles.)

___

As well, check out what happens when we look at GrLivArea (Above ground living area in sq. feet) vs SalePrice when sorted by HouseStyle - some styles are well represented in our dataset, others not so much, but we do see different sliding price scales for each HouseStyle given. 

<center>
	<img src="/assets/images/2020-08-05/GroundAreaSalePrice.png" width="100%"> 
</center>

In my exploration phase, other helpful bits of information I found:
* Utilities - only 1 house was listed with no Sewer or Water hookups, all 1459 other homes have all public utilities (not very helpful for dividing up our dataset into meaningful sub-trees)
* Street - only 6 homes are listed with gravel road access to the property, but this appears to greatly decrease the average SalePrice by around $50,000 (although this could be due to the extremely small comparative sample size)

<center>
	<img src="/assets/images/2020-08-05/StreetTypeSalePrice.png" width="40%"> 
</center>

* More home sales happen in the summer months than the winter (typical of the market in the Northern hemisphere, no one wants to move when it's 40º below freezing), but we're unsure of the relationship between the month of the sale and the sale price. 

<center>
	<img src="/assets/images/2020-08-05/HomesSoldPerMonth.png" width="49%"> <img src="/assets/images/2020-08-05/SalePricePerMonth.png" width="49%"> 
</center>

We can also see that the type of sale (TypeSale) can determine a different price bracket - good for our algorithm to recognize as well!

<center>
	<img src="/assets/images/2020-08-05/SalePriceSaleType.png" width='80%'>
</center>

Also good to note the top 3 SaleTypes:
* Conventional Warranty Deed - 1267
* New - 122
* Court Officer Deed / Estate - 43
Which means the number of the remaining SaleTypes is quite small in this dataset.

Now that I've had a good look at the dataset, I'm going to start reading <a href = "https://towardsdatascience.com/random-forest-in-python-24d0893d51c0"> this blog post </a> to give me a better idea of how to debug the Random Forest algorithm, and how I can interpret my results.

If you'd like any of the code I used to generate my graphs, I've posted it on my <a href="https://github.com/aimosjo/aimosjo.github.io/blob/master/assets/code/08-05-2020/graphingScript.py">github</a> under graphingScript.py. 

Thanks for reading! I'll leave you with a few pictures of my cats. This time, unrelated to RF or any ML algorithm - unless one comes out soon that deals with bread and/or toast.

<center>
	<img src="/assets/images/2020-08-05/bubby1.jpg" width= '45%'>
	<img src="/assets/images/2020-08-05/miss1.jpg" width= '45%'>
</center>

Until next time!
