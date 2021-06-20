
###############################################################################
#                                                                             #
#     nix-shell should run this to initialize the iowa home data train and    #
#     test sets, as well as loading necessary imports like pandas,            #
#     matplotlib, seaborn, and scikit-learn                                   #
#                                                                             #
###############################################################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from tabulate import tabulate

# read in the datasets
train_data_path = 'iowa-home-data/train.csv'
test_data_path = 'iowa-home-data/test.csv'

train_data = pd.read_csv(train_data_path)
test_data = pd.read_csv(test_data_path)

# create features dataframes, dropping SalePrice from train_features
train_features = train_data.drop(['SalePrice'], axis=1)
test_features = test_data

# merge the two data sets for analysis, and reset index
merge_data = pd.concat([train_features, test_features]).reset_index(drop=True)

###############################################################################
#                                                                             #
#                under here: code to fix NAs in the dataset so far            #
#                                                                             #
###############################################################################

none_cols = ['PoolQC', 'MiscFeature', 'Alley', 'Fence', 'FireplaceQu', 'GarageFinish', 'GarageQual', 'GarageCond', 'GarageType', 'BsmtCond', 'BsmtExposure', 'BsmtQual', 'BsmtFinType2', 'BsmtFinType1', 'MasVnrType'
]

for col in none_cols:
	train_data[col] = train_data[col].fillna("None")
	test_data[col] = test_data[col].fillna("None")
	merge_data[col] = merge_data[col].fillna("None")

###############################################################################

zero_cols = ['GarageYrBlt', 'MasVnrArea', 'BsmtFullBath', 'BsmtHalfBath', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF']

for col in zero_cols:
	train_data[col] = train_data[col].fillna(0, inplace=True)
	test_data[col] = test_data[col].fillna(0, inplace=True)
	merge_data[col] = merge_data[col].fillna(0, inplace=True)

###############################################################################
#                                 MSZoning                                    #
###############################################################################

# fillnas using mode of neighborhood's MSZoning variable

for ds in (test_data, train_data, merge_data):
	ds['MSZoning'] = ds['MSZoning'].fillna(ds.groupby('Neighborhood')['MSZoning'].transform(lambda x: x.mode().iloc[0]))

# check to make sure no more NAs exist for this variable
# for ds in (test_data, train_data, merge_data):
# 	print(ds[ds['MSZoning'].isna()])

###############################################################################
#                                Utilities                                    #
###############################################################################

test_data['Utilities'] = test_data['Utilities'].fillna('AllPub')

merge_data['Utilities'] = merge_data['Utilities'].fillna('AllPub')

###############################################################################
#                                 Functional                                  #
###############################################################################

condFeatures = ['Id', 'Functional', 'OverallCond', 'BsmtCond', 'ExterCond', 'GarageCond']

cond_map = {
	'None': 0,
	'Po': 1,
	'Fa':2,
	'TA':3,
	'Gd':4,
	'Ex':5
}
 # remap the categorical variables into integer variables
merge_data['BsmtCond'] = merge_data['BsmtCond'].map(cond_map).astype('int')
merge_data['ExterCond'] = merge_data['ExterCond'].map(cond_map).astype('int')
merge_data['GarageCond'] = merge_data['GarageCond'].map(cond_map).astype('int')

func_map = {
	'Sal'  : 0,
	'Sev'  : 1,
	'Maj2' : 2,
	'Maj1' : 3,
	'Mod'  : 4,
	'Min2' : 5,
	'Min1' : 6,
	'Typ'  : 7
}

mask5 = merge_data['Functional'].isna()
condfeatdf = merge_data[~mask5][condFeatures].copy()

condfeatdf['Functional'] = condfeatdf['Functional'].map(func_map).astype('int')

###############################################################################
#                          Exterior1st + Exterior2nd                          #
###############################################################################

mask6 = merge_data['Exterior1st'].isna()
mask7 = merge_data['Exterior2nd'].isna()
merge_data[mask6 & mask7][['ExterQual', 'ExterCond', 'Neighborhood', 'MSSubClass']]

mask8 = merge_data['Neighborhood'] == 'Edwards'
mask9 = merge_data['MSSubClass'] == 30
mask10 = merge_data['ExterQual'] == 'TA'
mask11 = merge_data['ExterCond'] == 3

# merge_data[mask8 & mask9 & mask10 & mask11][['Exterior1st', 'Exterior2nd']]

# fill in feature
mask12 = test_data['Id'] == 2152 # to find the original index in test_data

test_data.at[691, 'Exterior1st'] = 'Wd Sdng'
test_data.at[691, 'Exterior2nd'] = 'Wd Sdng'

merge_data.at[2151, 'Exterior1st'] = 'Wd Sdng'
merge_data.at[2151, 'Exterior2nd'] = 'Wd Sdng'

###############################################################################
#                                  Electrical                                 #
###############################################################################

# simply fill the na values with the mode

for ds in (test_data, train_data, merge_data):
	ds['Electrical'] = ds['Electrical'].fillna(ds['Electrical'].mode()[0])



###############################################################################
#                                 KitchenQual                                 #
###############################################################################

# simply fill the na values with the mode

for ds in (test_data, train_data, merge_data):
	ds['KitchenQual'] = ds['KitchenQual'].fillna(ds['KitchenQual'].mode()[0])


###############################################################################
#                                  SaleType                                   #
###############################################################################

# simply fill the na values with the mode

for ds in (test_data, train_data, merge_data):
	ds['SaleType'] = ds['SaleType'].fillna(ds['SaleType'].mode()[0])