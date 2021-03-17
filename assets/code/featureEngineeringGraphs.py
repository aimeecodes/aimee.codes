import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from tabulate import tabulate
from numpy.polynomial.polynomial import polyfit

# read in the datasets
train_data_path = 'iowa-home-data/train.csv'
test_data_path = 'iowa-home-data/test.csv'

test_data = pd.read_csv(test_data_path)
train_data = pd.read_csv(train_data_path)

# create features dataframes, dropping SalePrice from train_features
train_features = train_data.drop(['SalePrice'], axis=1)
test_features = test_data

# merge the two data sets for analysis, and reset index
merge_data = pd.concat([train_features, test_features]).reset_index(drop=True)

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

# set custom colour palette
Set2mod = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3', '#16425B', '#795C5F']

sns.set_palette(sns.color_palette(Set2mod))

LotConfigs = ['Inside', 'Corner', 'CulDSac', 'FR2', 'FR3']
merge_data['ScaledLotArea'] = merge_data['LotArea']/1000


########################################################################
#                                                                      #
#                pre-filled graphs are generated here                  #
#                                                                      #
########################################################################


# initialize index for counting graphs and changing colour
i=0

# begin loop to show subsetted graphs pre-filling NAs
# for lc in LotConfigs:

# 	# filter and assign data by each LotConfig
# 	filter1 = merge_data['LotConfig'] == lc
# 	filter2 = merge_data['ScaledLotArea'] <= 80
# 	filter3 = merge_data['LotFrontage'].isna()
# 	data = merge_data[filter1 & filter2 & ~filter3][['ScaledLotArea',
# 	'LotConfig',
# 	'LotFrontage']]

# 	plt.figure(figsize=(8,8))
# 	FrontageAreaPlot = plt.scatter(
# 		data['ScaledLotArea'],
# 		data['LotFrontage'],
# 		color=Set2mod[i],
# 		marker='o')

# 	b, m = polyfit(data['ScaledLotArea'],
# 		data['LotFrontage'], 1)

# 	plt.plot(
# 		data['ScaledLotArea'],
# 		b + m * data['ScaledLotArea'],
# 		'-',
# 		color=Set2mod[i])
# 	plt.xlim(0,80)
# 	plt.ylim(0,350)
# 	plt.ylabel(r'Lot Frontage in ft$\mathregular{^{2}}$')
# 	plt.xlabel(r'Lot Area in 1000 ft$\mathregular{^{2}}$')
# 	title = 'Lot Configuration: ' + lc
# 	plt.title(title)
# 	anno = 'y = ' + str(round(m,3)) + 'x + ' + str(round(b,3))

# 	plt.text(40,100,anno,color=Set2mod[i])
	
# 	# plt.show()

# 	# graphname = 'AreaFrontageSubplot' + str(i) + '.svg'
# 	# plt.savefig(graphname, format='svg')
# 	i=i+1

# function that takes in DataFrame, LotConfig and LotAreaScaled,
# and returns prediction for LotFrontage
def get_frontage_prediction(
	params,
	LotConfig,
	LotAreaScaled):
	# get b and m from params structure
	b = params.loc[LotConfig][0]
	m = params.loc[LotConfig][1]

	# return frontage_prediction as value
	return LotAreaScaled*m + b


# set array to all possible values of 'LotConfig' in the dataset
LotConfigs = ['Inside', 'Corner', 'CulDSac', 'FR2', 'FR3']

# create new column for LotArea scaled down by 1000 for all DataFrames
for ds in (
	merge_data,
	train_data,
	test_data):
	ds['ScaledLotArea'] = ds['LotArea']/1000

# initialize list to push all linear models to
lcparameters = []

# start loop to interate over all LotConfigs in merge_data
# note we are training this using all data found in merge_data
for lc in LotConfigs:

	# filter to only show data with specific LotConfig
	filter1 = merge_data['LotConfig'] == lc

	# filter to remove the outlier
	filter2 = merge_data['ScaledLotArea'] <= 80

	# filter to remove all NAs (so they're not used in our predictions)
	filter3 = merge_data['LotFrontage'].isna()

	# assign the intersection of these slices to data, keep three columns
	data = merge_data[filter1 & filter2 & ~filter3][['ScaledLotArea',
	'LotConfig',
	'LotFrontage']]

	# use polyfit to get coefficients of linear model based on sliced data
	b, m = polyfit(data['ScaledLotArea'],
		data['LotFrontage'], 1)

	# push these coefficients w/ lc ('LotConfig') as tuples to list
	lcparameters += [[b, m]]

# linear_model_parameters
# make list into DataFrame for easier access
lm_params = pd.DataFrame(
	lcparameters,
	index = LotConfigs,
	columns = ['b', 'm']
	)

# fill using fillna transform rule
for ds in (
  test_data,
  train_data,
  merge_data):
	ds['LotFrontage'] = \
	  ds['LotFrontage'].fillna(
	  	ds.apply(
	  		lambda x: get_frontage_prediction(
	  			lm_params,
	  			x.loc['LotConfig'],
	  			x.loc['ScaledLotArea']),
	  		axis=1))

 # generate new plots to see how LotFrontage is filled according to the new
 # rule 


###############################################################################
##            IN THIS BLOCK, ALL CODE IS USED TO GENERATE GRAPHS             ##
###############################################################################
# initialize index i for saving graphs and moving through color palette
i=0

for lc in LotConfigs:

	# filter to only show data with specific LotConfig
	filter1 = merge_data['LotConfig'] == lc

	# filter to remove the outlier
	filter2 = merge_data['ScaledLotArea'] <= 80

	# filter to remove all NAs (so they're not used in our predictions)
	filter3 = merge_data['LotFrontage'].isna()

	# assign the intersection of these slices to data, keep three columns
	data = merge_data[filter1 & filter2 & ~filter3][['ScaledLotArea',
	'LotConfig',
	'LotFrontage']]

	# check out new generated plots
	b, m = polyfit(data['ScaledLotArea'],
		data['LotFrontage'], 1)

	plt.figure(figsize=(8,8))
	plt.plot(
		data['ScaledLotArea'],
		b + m * data['ScaledLotArea'],
		'-',
		color='Grey')

	FrontageAreaPlot = plt.scatter(
		data['ScaledLotArea'],
		data['LotFrontage'],
		color=Set2mod[i],
		marker='o')
	plt.xlim(0,80)
	plt.ylim(0,350)
	plt.ylabel(r'Lot Frontage in ft$\mathregular{^{2}}$ (Filled)')
	plt.xlabel(r'Lot Area in 1000 ft$\mathregular{^{2}}$')
	title = 'Lot Configuration: ' + lc
	plt.title(title)

	anno = 'y = ' + str(round(m,3)) + 'x + ' + str(round(b,3))
	plt.text(40,100,anno,color='Grey')
	
	# plt.show()

	graphname = 'AreaFrontageSubplotPostFill' + str(i) + '.svg'
	plt.savefig(graphname, format='svg')
	i=i+1
###############################################################################
##            IN THIS BLOCK, ALL CODE IS USED TO GENERATE GRAPHS             ##
###############################################################################