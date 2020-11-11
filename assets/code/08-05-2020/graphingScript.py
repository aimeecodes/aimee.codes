import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# read in the datasets
train_data_path = 'iowa-home-data/train.csv'
test_data_path = 'iowa-home-data/test.csv'

train_data = pd.read_csv(train_data_path)
test_data = pd.read_csv(test_data_path)

###########################################################
#                      INSTRUCTIONS                       #
#                                                         #
# to view each graph, uncomment the code and run          #
# graphingScript.py using python3                         # 
#                                                         #
# types of plots are separated by                         #
#  ###############                                        #
#  #  plot type  #                                        #
#  ###############                                        #
#                                                         #
# plots within the same type are separated by hashes #### #
#                                                         #
###########################################################


###########################################################
#                    Basic Category Plot                  #
###########################################################

# #1. Create a boxplot that compares Fireplace (number of fireplaces) to SalePrice (selling price of the home), and sorts them by FireplaceQu (low to high quality of fireplaces)

# fireplaceQuOrder = ['Po', 'Fa', 'TA', 'Gd', 'Ex']

# print(train_data['FireplaceQu'].value_counts())

# fpPlot = sns.catplot(x='Fireplaces', y='SalePrice', data=train_data, palette='muted', hue='FireplaceQu', hue_order=fireplaceQuOrder, kind='box')

# # change x-axis so we don't have 0 fireplaces plotted
# plt.xlim(0.5,3.5)

# plt.show()

###########################################################

# # 2. Create a boxplot that compares SalePrice of houses with Paved vs. Gravel access roads

# # Use variable feat to keep track of the feature you're plotting
# feat = 'Street'

# StreetType = ['Paved', 'Gravel']

# print(train_data[feat].value_counts())

# stPlot = sns.catplot(x=feat, y='SalePrice', data=train_data, kind='box')
# f.set_xticklabels(StreetType)
# plt.title('StreetType vs. SalePrice')

# plt.show()

###########################################################

# # 3. Compare the functionality (Functional) of the home to the SalePrice, in order of Salvage > Severe > Major2 > Major 1 > Minor 2 > Minor 1 > Typical

# feat = 'Functional'
# FuncOrder = ['Sal', 'Sev', 'Maj2', 'Maj1', 'Min2', 'Min1', 'Typ']

# print(train_data[feat].value_counts())

# funcPlot = sns.catplot(x=feat, y='SalePrice', data=train_data, kind='box', order = FuncOrder)
# # funcPlot.set_xticklabels(StreetType)
# plt.xlabel('Functionality')
# plt.title('Functionality vs. SalePrice')

# plt.show()

###########################################################

# # 4. Compare the distribution of SalePrice sorted by MoSold (month of sale)

# print(train_data['MoSold'].value_counts())

# moSalePlot = sns.catplot(x='MoSold', y='SalePrice', data=train_data, palette='muted', kind='violin')
# plt.xlabel('Month Sold')
# plt.ylabel('Sale Price')
# plt.title('Housing Sale Prices Per Month')
# plt.show()

# # 4.5. Compare the distribution of SalePrice sorted by OverallQual (month of sale)

# print(train_data['OverallQual'].value_counts())

# OverQuPlot = sns.catplot(x='OverallQual', y='SalePrice', data=train_data, palette='muted', kind='box')
# plt.xlabel('Overall Quality')
# plt.ylabel('Sale Price')
# plt.title('Housing Sale Prices\nSorted by Overall Quality')
# plt.show()

###########################################################

# # 5. Compare the distribution of SalePrice of different SaleTypes
# SaleTypeLabels=['WD\nConventional', 'WD\nCash', 'WD\nVA Loan', 'New', 'Estate', 'Contract\n15% Down', 'Contract\nLow Down\nLow Interest', 'Contract\n Low Interest', 'Contract\nLow Down', 'Other']

# salePlot = sns.catplot(x='SaleType', y='SalePrice', data=train_data, palette='muted', kind='boxen', order=['WD', 'CWD', 'VWD', 'New', 'COD', 'Con', 'ConLw', 'ConLI', 'ConLD', 'Oth'])
# plt.xlabel('Sale Type')
# salePlot.set_xticklabels(SaleTypeLabels)
# plt.ylabel('Sale Price')
# plt.title('Sale Prices by Sale Type')
# plt.show()
###########################################################
#                   Linear Regression Plot                #
###########################################################

# # 6. Plot SalePrice against GarageArea, sort by GarageType, and use linearReg to visualize the trend of the relationship

# GarageTypeLabels = ['Attached', 'Detatched', 'Built-in', 'Car Port', 'Basement', '2 Types']

# garagePlot = sns.lmplot(x='GarageArea', y='SalePrice', data=train_data, palette='muted', hue='GarageType', legend=False)
# plt.legend(labels=GarageTypeLabels)
# plt.xlim(0,1500)
# plt.title('Garage Area and Sale Price, Sorted by Garage Type')

# plt.show()

###########################################################

# # 7. Plot SalePrice against GrLiveArea (living area above ground), sort by HouseStyle, and use linearReg to visualize the trend of the relationship

# LiveAreaPlot = sns.lmplot(x='GrLivArea', y='SalePrice', data=train_data, palette='muted', col='HouseStyle', hue='HouseStyle', col_wrap=4, legend=True)

# plt.show()

###########################################################

# # 8. Plot SalePrice against LotArea, sort by MSZoning (General zoning classification of the sale), and use linearReg to visualize the trend of the relationship (if any)

# # NOTE - without filtering, this plot doesn't give a great idea of trends, since there are some outliers in lotArea that make it hard to see the trend among the typical lotAreas
# # [to solve this, we filter out lots that are larger than 25000 sq ft]

# mask = train_data['LotArea'] <= 25000
# under50000 = train_data[mask]
# over500000 = train_data[~mask]

# lotAreaPlot = sns.lmplot(x='LotArea', y='SalePrice', data=under50000, palette='muted', hue='MSZoning')

# plt.ylim(0, max(train_data['SalePrice'])+25000)

# plt.show()

###########################################################
#                      Countplot                          #
###########################################################

# # 9. Count the number of homes in each BldgType category

# BldgTypeLabels = ['Single-family\n Detatched', 'Two-family\n Conversion', 'Duplex', 'Townhouse\n End Unit', 'Townhouse\n Inside Unit']

# create a countplot for BldgType
# f = sns.countplot(x='BldgType', data=train_data)
# f.set_xticklabels(BldgTypeLabels)
# plt.title('Number of Each Building Type in Dataset')
# plt.xlabel('Building Types')
# plt.ylabel('Count')

# # label the count bars with the count
# for p, label in zip(f.patches, train_data['BldgType'].value_counts().index):
# 	f.annotate(p.get_height(), (p.get_x()+0.1, p.get_height()+9))

# plt.show()

###########################################################

# # 9.5. Count the number of homes in each OverallQual category

# # create a countplot for OVerallQual
# ov = sns.countplot(x='OverallQual', data=train_data)
# plt.title('Number of Examples of Overall Quality Rating\n1-10')
# plt.xlabel('Quality Rating')
# plt.ylabel('Count')

# # label the count bars with the count
# for p, label in zip(ov.patches, train_data['OverallQual'].value_counts().index):
# 	ov.annotate(p.get_height(), (p.get_x()+0.1, p.get_height()+9))

# plt.show()

###########################################################

# # 10. Count the number of homes sold in each month (MoSold)

# r = sns.countplot(x='MoSold', data=train_data, palette='muted')

#plt.ylim(0,300)
#for p, label in zip(r.patches, train_data['MoSold'].value_counts().index):
# 	r.annotate(p.get_height(), (p.get_x()+0.1, p.get_height()+9))
#plt.xlabel('Month')
#plt.ylabel('Number of Homes Sold')
#plt.title('Number of Homes Sold per Month')

#plt.show()