import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from numpy.polynomial.polynomial import polyfit

# set overall font sizes

# small graphs >>> 28, 30, 32
# figsize=(12,12) >>> 22, 24, 26
# oversized >>> 18, 20, 22
SMALL_SIZE = 18
MEDIUM_SIZE = 20
BIGGER_SIZE = 22

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

# read in the datasets
train_data_path = 'iowa-home-data/train.csv'
test_data_path = 'iowa-home-data/test.csv'

train_data = pd.read_csv(train_data_path)
test_data = pd.read_csv(test_data_path)

# set custom colour palette
Set2mod = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3', '#16425B', '#795C5F']

sns.set_palette(sns.color_palette(Set2mod))

train_data['ScaledSalePrice'] = train_data['SalePrice']/100000

###############################################################################

############## 1 (A) - SalePrice Sorted by OverallQual ########################

# plt.figure(figsize=(12,12))
# OverQuPlot = sns.boxplot(
# 	x='OverallQual',
# 	y='ScaledSalePrice',
# 	data=train_data,
# 	linewidth='1')

# plt.xlabel('Quality Rating')
# plt.ylabel('Sale Price\nin $100,000s')
# plt.yticks(np.arange(0,8,1))
# plt.title('Housing Sale Prices\nSorted by Overall Quality 1-10')
# # plt.show()
# plt.savefig('OverallQualSalePrice.svg', format='svg')

############## 1 (B) - OverallQual Count ######################################

# plt.figure(figsize=(12,12))
# ov = sns.countplot(
# 	x='OverallQual',
# 	data=train_data)
# plt.title('Number of Examples with\nOverall Quality Rating 1-10')
# plt.xlabel('Quality Rating')
# plt.ylabel('Count')

# # label the count bars with the count
# for p, label in zip(ov.patches, train_data['OverallQual'].value_counts().index):
# 	ov.annotate(p.get_height(), (p.get_x()+0.1, p.get_height()+8))
# # plt.show()
# plt.savefig('OverallQualCount.svg', format='svg')

############## 2 (A) SalePrice by BldgType ####################################

# train_data['ScaledSalePrice'] = train_data['SalePrice']/100000
# BldgTypeLabels = ['Single-family\n Detatched', 'Two-family\n Conversion', 'Duplex', 'Townhouse\n End Unit', 'Townhouse\n Inside Unit']

# plt.figure(figsize=(12,12))
# BldgTypePlot = sns.boxenplot(
# 	x='BldgType',
# 	y='ScaledSalePrice',
# 	data=train_data,
# 	linewidth='1')

# plt.xlabel('Building Type')
# BldgTypePlot.set_xticklabels(BldgTypeLabels)
# plt.ylabel('Sale Price\nin $100,000s')
# plt.yticks(np.arange(0,8,1))
# plt.title('Housing Sale Prices\nSorted by Building Type')
# # plt.show()
# plt.savefig('BldgTypeSalePrice.svg', format='svg')

############## 2 (B) BldgType Count ###########################################

# BldgTypeLabels = ['Single-family\n Detatched', 'Two-family\n Conversion', 'Duplex', 'Townhouse\n End Unit', 'Townhouse\n Inside Unit']

# # # create a countplot for BldgType
# plt.figure(figsize=(12,12))
# f = sns.countplot(
# 	x='BldgType',
# 	data=train_data)
# f.set_xticklabels(BldgTypeLabels)
# plt.title('Number of Examples of\nBuilding Type in train_data')
# plt.xlabel('Building Types')
# plt.ylabel('Count')

# # label the count bars with the count
# for p, label in zip(f.patches, train_data['BldgType'].value_counts().index):
# 	f.annotate(p.get_height(), (p.get_x()+0.1, p.get_height()+8))

# # plt.show()
# plt.savefig('BldgTypeCount.svg', format='svg')

############## (3) SalePrice by GarageArea + Garage Type ######################

# # #                  decrease font sizes to 18, 20, 22                  # # #

# GarageTypeLabels = ['Attached', 'Detatched', 'Built-in', 'Car Port', 'Basement', '2 Types']
# train_data['ScaledSalePrice'] = train_data['SalePrice']/100000

# garagePlot = sns.lmplot(
# 	x='GarageArea',
# 	y='ScaledSalePrice',
# 	data=train_data,
# 	hue='GarageType',
# 	legend=False,
# 	height=8,
# 	aspect=2)

# plt.legend(labels=GarageTypeLabels)
# plt.ylabel('Sale Price in $100,000s')
# plt.xlabel(r'Garage Area in ft$\mathregular{^{2}}$')
# plt.xlim(0,1500)
# plt.yticks(np.arange(0,8,1))
# plt.title('Garage Area and Sale Price, Sorted by Garage Type')

# # plt.show()
# plt.savefig('GarageAreaGarageTypeLinearReg.svg', format='svg')

############## (4) SalePrice by GrLivArea + HouseStyle ########################

# # #                  increase font sizes to 28, 30, 32                  # # #

# # HouseStyles = train_data['HouseStyle'].value_counts().index.values.tolist()

# HouseStyles = ['1Story', '1.5Fin', '2.5Fin', 'SFoyer', '2Story', '1.5Unf', '2.5Unf', 'SLvl']

# i=0
# for hs in HouseStyles:

# 	# filter and assign data by each HouseStyle
# 	data = train_data[train_data['HouseStyle'] == hs][['GrLivArea', 'HouseStyle','ScaledSalePrice']]

# 	plt.figure(figsize=(8,8))
# 	LivAreaPlot = plt.scatter(
# 		data['GrLivArea'],
# 		data['ScaledSalePrice'],
# 		color=Set2mod[i],
# 		marker='o')
# 	b, m = polyfit(data['GrLivArea'],
# 		data['ScaledSalePrice'], 1)
# 	plt.plot(
# 		data['GrLivArea'],
# 		b + m * data['GrLivArea'],
# 		'-',
# 		color=Set2mod[i])
# 	plt.ylabel('Sale Price in $100,000s')
# 	plt.yticks(np.arange(0,8,1))
# 	plt.xlim(0, 5000)
# 	plt.xlabel(r'Above Ground Living Area in ft$\mathregular{^{2}}$')
# 	title = 'House Style: ' + hs
# 	plt.title(title)
	
# 	# plt.show()

# 	graphname = 'GrLivAreaSubplot' + str(i) + '.svg'
# 	plt.savefig(graphname, format='svg')
# 	i=i+1

##############       (5) Street Type + Sale Price      ########################

# StreetType = ['Paved', 'Gravel']

# plt.figure(figsize=(10,10))
# stPlot = sns.boxenplot(x='Street',
# 	y='ScaledSalePrice',
# 	data=train_data)

# stPlot.set_xticklabels(StreetType)
# plt.xlabel('Street Type')
# plt.title('Sale Price Sorted by Street Type')
# plt.ylabel('Sale Price in $100,000s')
# plt.yticks(np.arange(0,8,1))

# # # plt.show()
# plt.savefig('SalePriceStreet.svg', format='svg')

##################### 6 (A) Number of Homes Sold per Month ####################

# plt.figure(figsize=(12,12))
# r = sns.countplot(
# 	x='MoSold',
# 	data=train_data)

# plt.ylim(0,300)
# for p, label in zip(r.patches, train_data['MoSold'].value_counts().index):
# 	r.annotate(p.get_height(), (p.get_x()+0.1, p.get_height()+9))
# plt.xlabel('Month')
# plt.ylabel('Number of Homes Sold')
# plt.title('Number of Homes Sold per Month')

# # # plt.show()
# plt.savefig('HomesSoldPerMonth.svg', format='svg')

##################### 6 (B) House Price Sales per Month #######################

# plt.figure(figsize=(12,12))
# moSalePlot = sns.violinplot(x='MoSold',
# 	y='ScaledSalePrice',
# 	data=train_data)

# plt.xlabel('Month Sold')
# plt.title('Housing Sale Prices Per Month')
# plt.ylim(0,8)
# plt.ylabel('Sale Price in $100,000s')
# plt.yticks(np.arange(0,8,1))

# # plt.show()
# plt.savefig('SalePriceMonth.svg', format='svg')


#####################   (7) SalePrice by SaleType   ###########################

# SaleTypeLabels=['Warranty Deed Conventional', 'Warranty Deed Cash', 'Warranty Deed VA Loan', 'New', 'Estate', 'Contract 15% Down', 'Contract Low Down Low Interest', 'Contract Low Interest', 'Contract Low Down', 'Other']
SaleTypeValues=['WD', 'CWD', 'VWD', 'New', 'COD', 'Con', 'ConLw', 'ConLI', 'ConLD', 'Oth']

# print(dict(zip(SaleTypeValues, SaleTypeLabels)))

# plt.figure(figsize=(15,10))
# salePlot = sns.boxenplot(x='SaleType',
# 	y='ScaledSalePrice',
# 	data=train_data,
# 	order=SaleTypeValues)
# plt.xlabel('Sale Type')
# # salePlot.set_xticklabels(SaleTypeLabels)
# plt.xticks(rotation=45)
# plt.ylim(0,8)
# plt.ylabel('Sale Price in $100,000s')
# plt.yticks(np.arange(0,8,1))
# plt.title('Sale Prices by Sale Type')
# # # plt.show()
# plt.savefig('SalePriceSaleType.svg', format='svg')