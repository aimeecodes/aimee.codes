# for data exploration
import pandas as pd

# for numerical manip
import numpy as np

# for graphing
import matplotlib.pyplot as plt
import seaborn as sns

# for importing modules from ../modules
import sys
sys.path.insert(1, '../modules')

# for making dataframes the way I like them
from cleaning import importCSVandRemoveWhiteSpace

# read in the dataset, make dataframe, and remove whitespace from columns
fulldatadf = importCSVandRemoveWhiteSpace('../iowa-home-data/fullset.csv')

# list of irrelevant columns
irr_cols = ['Order']

# drop irrelevant columns
from cleaning import dropIrrelevantColumns

dropIrrelevantColumns(fulldatadf, irr_cols)

##############################################################
#                FILL CATEGORICAL NAs WITH NONE              #
##############################################################

from cleaning import fillCatNAwithNone

none_cols = [
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
	'BsmtFinType2',
	'BsmtFinType1',
	'MasVnrType']

fillCatNAwithNone(fulldatadf, none_cols)


##############################################################
#                  FILL NUMERICAL NAs WITH ZERO              #
##############################################################

from cleaning import fillNumNAwithZero

zero_cols = [
    'GarageYrBlt',
    'MasVnrArea',
    'BsmtFullBath',
    'BsmtHalfBath',
    'BsmtFinSF1',
    'BsmtFinSF2',
    'BsmtUnfSF',
    'TotalBsmtSF',
    'LotFrontage']

fillNumNAwithZero(fulldatadf, zero_cols)


##############################################################
#              FILTER NUMERICAL NAs - GRAPH BASED            #
##############################################################

from cleaning import removeIQROutliersFromDF
from cleaning import makeFilters
from cleaning import makeIQROutlierPairs

# have to make some graphs in order to determine outliers in the dataset
# here we are only examining LotArea and GrLivArea (above ground living area)

# create dataframe for examining outliers
exoutdf = pd.DataFrame(fulldatadf[['GrLivArea', 'LotArea', 'SalePrice']])

# create column to flag outliers
exoutdf['GrLivOutlier'] = exoutdf['GrLivArea'] >= 4000
exoutdf['LotAreaOutlier'] = exoutdf['LotArea'] >= 80000
exoutdf['GrLivLogArea'] = exoutdf['GrLivArea'].apply(lambda x: np.log(x))
exoutdf['LotLogArea'] = exoutdf['LotArea'].apply(lambda x: np.log(x))
exoutdf['GrLivIQROutlier'], exoutdf['LotAreaIQROutlier'] = makeFilters(
    exoutdf,
    makeIQROutlierPairs(exoutdf,
                        ['GrLivArea',
                         'LotArea']))
exoutdf['GrLivIQROutlier'] = ~exoutdf['GrLivIQROutlier']
exoutdf['LotAreaIQROutlier'] = ~exoutdf['LotAreaIQROutlier']

axislabelssize = 14
generateLotAreaGrLivArea = False
if generateLotAreaGrLivArea:
    plt.rc('xtick', labelsize = axislabelssize)
    plt.rc('ytick', labelsize = axislabelssize)

    fig, (ax1, ax2) = plt.subplots(nrows=1,
                                   ncols=2,
                                   sharex=False,
                                   figsize=(14,8))
    plt.figure(figsize=(12,8))

    # set color palette
    pal = sns.color_palette('Set2')

    sns.scatterplot(ax = ax1,
                    x='GrLivArea',
                    y='SalePrice',
                    data=exoutdf,
                    palette = sns.color_palette('Set2', 2),
                    hue = 'GrLivIQROutlier',
                    style = 'GrLivOutlier',
                    size = 'GrLivOutlier',
                    sizes = [15, 150],
                    markers = ['o', '*'])
    ax1.set_xlabel('Above Ground Living Area', fontsize=14)
    ax1.set_ylabel('Sale Price', fontsize = 14)
    ax1.set_title('Sale Price vs. Above Ground Living Area', fontsize=16)
    ax1.legend(loc = 'upper left',
               fontsize = 12)

    sns.scatterplot(ax = ax2,
                    x='LotArea',
                    y='SalePrice',
                    data=exoutdf,
                    palette = sns.color_palette('Set2', 2),
                    hue = 'LotAreaIQROutlier',
                    style = 'LotAreaOutlier',
                    size = 'LotAreaOutlier',
                    sizes = [15, 150],
                    markers = ['o', '*'])
    ax2.set_xlabel('Lot Area', fontsize = 14)
    ax2.set_ylabel('Sale Price', fontsize = 14)
    ax2.set_title('Sale Price vs. Lot Area', fontsize=16)
    ax2.legend(loc = 'upper right',
                fontsize = 12)

    title = 'Checking for Outliers'
    fig.suptitle(title, fontsize = 20)
    fig.tight_layout()

    filename = 'CheckingforOutliersScatterPlot.svg'
    fig.savefig(filename, format='svg')

generateLogLotAreaGrLivArea = False
if generateLogLotAreaGrLivArea:
    plt.rc('xtick', labelsize = axislabelssize)
    plt.rc('ytick', labelsize = axislabelssize)

    fig, (ax1, ax2) = plt.subplots(nrows=1,
                                   ncols=2,
                                   sharex=False,
                                   figsize=(14,8))
    plt.figure(figsize=(12,8))

    # set color palette
    pal = sns.color_palette('Set2')

    sns.scatterplot(ax = ax1,
                    x='GrLivLogArea',
                    y='SalePrice',
                    data=exoutdf,
                    palette = sns.color_palette('Set2', 2),
                    hue = 'GrLivIQROutlier',
                    style = 'GrLivOutlier',
                    size = 'GrLivOutlier',
                    sizes = [15, 150],
                    markers = ['o', '*'])
    ax1.set_xlabel('Log of Above Ground Living Area', fontsize=14)
    ax1.set_ylabel('Sale Price', fontsize = 14)
    ax1.set_title('Sale Price vs. Log of Above Ground Living Area', fontsize=16)
    ax1.legend(loc = 'upper left',
               fontsize = 12)

    sns.scatterplot(ax = ax2,
                    x='LotLogArea',
                    y='SalePrice',
                    data=exoutdf,
                    palette = sns.color_palette('Set2', 2),
                    hue = 'LotAreaIQROutlier',
                    style = 'LotAreaOutlier',
                    size = 'LotAreaOutlier',
                    sizes = [15, 150],
                    markers = ['o', '*'])
    ax2.set_xlabel('Log of Lot Area', fontsize = 14)
    ax2.set_ylabel('Sale Price', fontsize = 14)
    ax2.set_title('Sale Price vs. Log of Lot Area', fontsize=16)
    ax2.legend(loc = 'upper right',
                fontsize = 12)

    title = 'Checking for Logarithmic Outliers'
    fig.suptitle(title, fontsize = 20)
    fig.tight_layout()

    filename = 'CheckingforLogOutliersScatterPlot.svg'
    fig.savefig(filename, format='svg')

# these are continuous numerical features that need to be
# filtered for outliers so that analysis is consistent
# needIQRfiltering_cols = [
    # 'LotArea',
    # 'GrLivArea']

# remove all samples with outliers from the dataset
# fulldatadf = removeIQROutliersFromDF(
    # fulldatadf,
    # needIQRfiltering_cols)

# NEW RULE: do not use IQR filtering, instead use the following
grlivareafilter = fulldatadf['GrLivArea'] >= 4000
salepricefilter = fulldatadf['SalePrice'] <= 200000
lotareafilter   = fulldatadf['LotArea']   >= 80000

# filter out these outliers
fulldatadf = fulldatadf[~((grlivareafilter & salepricefilter) | lotareafilter)]

##############################################################
#               FILL CAT NAs WITH MODE OF CATEGORY           #
##############################################################

from cleaning import fillCatNAwithModeList

mode_cols = [
    'Electrical',]

fillCatNAwithModeList(fulldatadf, mode_cols)

##############################################################
#        HANDLE REMAINING NAs (GARAGE CARS / AREA)           #
##############################################################

from cleaning import fillDiscreteNAwithMode, fillContNAwithMean

fillDiscreteNAwithMode(fulldatadf, 'GarageCars', 'GarageType')

fillContNAwithMean(fulldatadf, 'GarageArea', 'GarageType')

##############################################################
#                      HANDLE MSZONING                       #
##############################################################

# filter out commercial, industrial, and agricultural properties
MSZoning_cols = ['RL', 'RM', 'FV', 'RH']

MSZoning_mask = fulldatadf['MSZoning'].isin(MSZoning_cols)

fulldatadf = fulldatadf[MSZoning_mask]

##############################################################
#          Remapping Ordinal Features to Numerical           #
##############################################################

from cleaning import remapCommonDict, remap

# define condition and quality map,
# many features use this rating system of 0-5
cond_qual_map = {
    'None' : 0,
    'Po'   : 1,
    'Fa'   : 2,
    'TA'   : 3,
    'Gd'   : 4,
    'Ex'   : 5
}

# these are columns that can use the same dictionary
# to map between ordinal and discrete numerical
cond_qual_cols = [
    'ExterQual',
    'ExterCond',
    'BsmtQual',
    'BsmtCond',
    'HeatingQC',
    'KitchenQual',
    'FireplaceQu',
    'GarageQual',
    'GarageCond',
    'PoolQC']

remapCommonDict(fulldatadf,
                       cond_qual_cols,
                       cond_qual_map)

# convert BsmtFinType1 and BsmtFinType2 to numerical
bsmtfintype_map = {
        'None' : 0,
        'Unf'  : 1,
        'LwQ'  : 2,
        'Rec'  : 3,
        'BLQ'  : 4,
        'ALQ'  : 5,
        'GLQ'  : 6
}

bsmt_fin_cols = ['BsmtFinType1', 'BsmtFinType2']

remapCommonDict(fulldatadf,
                       bsmt_fin_cols,
                       bsmtfintype_map)

# convert Electrical to numerical
electrical_map = {
        'Mix'   : 1,
        'FuseP' : 2,
        'FuseF' : 3,
        'FuseA' : 4,
        'SBrkr' : 5
}

remap(fulldatadf,
             'Electrical',
             electrical_map)


# convert Functional to numerical, merging 'Sev' 'Maj1' and 'Maj2'
functional_map = {
        'Sal'  : 1,
        'Sev'  : 2,
        'Maj2' : 3,
        'Maj1' : 4,
        'Mod'  : 5,
        'Min2' : 6,
        'Min1' : 7,
        'Typ'  : 8
}

remap(fulldatadf,
             'Functional',
             functional_map)

# convert GarageFinish to numerical
garagefin_map = {
        'None' : 0,
        'Unf'  : 1,
        'RFn'  : 2,
        'Fin'  : 3
}

remap(fulldatadf,
             'GarageFinish',
             garagefin_map)

# convert PavedDrive to numerical
paveddrive_map = {
        'N' : 1,
        'P' : 2,
        'Y' : 3
}

remap(fulldatadf,
             'PavedDrive',
             paveddrive_map)

# convert Fence to numerical
fence_map = {
        'None'  : 0,
        'MnWw'  : 1,
        'GdWo'  : 2,
        'MnPrv' : 3,
        'GdPrv' : 4
}

remap(fulldatadf,
             'Fence',
             fence_map)

##############################################################
#   Merging Low Cardinality Levels within Nominal Factors    #
##############################################################

# this section continues to use remap, this time with a string
# as the datatype

roofstyle_map = {
        'Gable'   : 'Gable',
        'Hip'     : 'Hip',
        'Gambrel' : 'Gambrel',
        'Mansard' : 'Mansard',
        'Flat'    : 'Shed',
        'Shed'    : 'Shed'
        }

remap(fulldatadf,
      'RoofStyle',
      roofstyle_map,
      'str')


roofmatl_map = {
        'CompShg' : 'CompShg',
        'Tar&Grv' : 'Other',
        'WdShake' : 'Other',
        'WdShngl' : 'Other',
        'Metal'   : 'Other',
        'ClyTile' : 'Other',
        'Membran' : 'Other',
        'Roll'    : 'Other'
        }

remap(fulldatadf,
      'RoofMatl',
      roofmatl_map,
      'str')

# fix typos in Exterior1st and Exterior2nd
exter_typos = {
    'AsbShng'  : 'AsbShng',
    'AsphShn'  : 'AsphShn',
    'Brk Cmn'  : 'BrkComm',
    'BrkComm'  : 'BrkComm',
    'BrkFace'  : 'BrkFace',
    'CBlock'   : 'CBlock',
    'CmentBd'  : 'CemntBd',
    'CemntBd'  : 'CemntBd',
    'HdBoard'  : 'HdBoard',
    'ImStucc'  : 'ImStucc',
    'MetalSd'  : 'MetalSd',
    'Other'    : 'Other',
    'Plywood'  : 'Plywood',
    'PreCast'  : 'PreCast',
    'Stone'    : 'Stone',
    'Stucco'   : 'Stucco',
    'VinylSd'  : 'VinylSd',
    'Wd Sdng'  : 'Wd Sdng',
    'Wd Shng'  : 'WdShing',
    'WdShing'  : 'WdShing'
    }

remapCommonDict(fulldatadf,
                ['Exterior1st',
                 'Exterior2nd'],
                exter_typos,
                'str')

# # exploratory intermediate values for ex1 and ex2
# exterior_mask = fulldatadf.apply(lambda x: x['Exterior2nd'] == x['Exterior1st'], axis=1)
# extpairs = fulldatadf[~exterior_mask][['Exterior1st', 'Exterior2nd']].values
# for i in range(0, len(extpairs)):
#     extpairs[i] = np.sort(extpairs[i])

exterior_map = {
    'AsbShng'  : 'AsbShng',
    'AsphShn'  : 'Other',
    'BrkComm'  : 'Brick',
    'BrkFace'  : 'Brick',
    'CBlock'   : 'Other',
    'CemntBd'  : 'CemntBd',
    'HdBoard'  : 'HdBoard',
    'ImStucc'  : 'Other',
    'MetalSd'  : 'MetalSd',
    'Other'    : 'Other',
    'Plywood'  : 'Plywood',
    'PreCast'  : 'Other',
    'Stone'    : 'Other',
    'Stucco'   : 'Stucco',
    'VinylSd'  : 'VinylSd',
    'Wd Sdng'  : 'Wd Sdng',
    'WdShing'  : 'WdShing',
    }

remapCommonDict(fulldatadf,
                ['Exterior1st',
                 'Exterior2nd'],
                exterior_map,
                'str')

# assuming ext2 has the same importance as ext1,
# can exchange them so that they are alphabetical pairs

# get the values
exteriorpairs = fulldatadf[['Exterior1st',
                            'Exterior2nd']].values

# sort the values pair by pair
for i in range(0, len(exteriorpairs)):
    exteriorpairs[i] = np.sort(exteriorpairs[i])

# reassign the values
fulldatadf[['Exterior1st',
            'Exterior2nd']] = exteriorpairs

masvnrtype_map = {
    'None'    : 'None',
    'BrkFace' : 'Brick',
    'Stone'   : 'Stone',
    'BrkCmn'  : 'Brick',
    'CBlock'  : 'Stone'
    }

remap(fulldatadf,
      'MasVnrType',
      masvnrtype_map,
      'str')

foundation_map = {
    'PConc'  : 'PConc',
    'CBlock' : 'CBlock',
    'BrkTil' : 'BrkTil',
    'Slab'   : 'Slab',
    'Stone'  : 'Other',
    'Wood'   : 'Other'
    }

remap(fulldatadf,
      'Foundation',
      foundation_map,
      'str')

heating_map = {
    'GasA'  : 'GasA',
    'GasW'  : 'GasW',
    'Grav'  : 'Other',
    'Wall'  : 'Other',
    'OthW'  : 'Other',
    'Floor' : 'Other'
    }

remap(fulldatadf,
      'Heating',
      heating_map,
      'str')

centralair_map = {
    'Y' : 1,
    'N' : 0
    }

remap(fulldatadf,
      'CentralAir',
      centralair_map,
      'str')

##############################################################
#                SaleType - Needs Graphing                   #
##############################################################
saletypeorder_premerge = ['WD ',
                          'CWD',
                          'VWD',
                          'New',
                          'COD',
                          'Con',
                          'ConLw',
                          'ConLI',
                          'ConLD',
                          'Oth']

# specify the type of graph to be generated,
# and parameters to be passed in
axislabelssize = 14

# specify if graphs should be generated
generatesaletypegraph = False

if generatesaletypegraph:
    plt.rc('xtick', labelsize = axislabelssize)
    plt.rc('ytick', labelsize = axislabelssize)

    fig, ax = plt.subplots()
    plt.figure(figsize=(12,8))

    tab = fulldatadf['SaleType'].value_counts()

    # set color palette
    pal = sns.color_palette('Set2', len(tab))

    ax = sns.boxplot(x='SaleType',
                     y='SalePrice',
                     data=fulldatadf,
                     order = tab[saletypeorder_premerge].index,
                     palette = pal)

    plt.xlabel('SaleType', fontsize = 18)
    plt.ylabel('Sale Price', fontsize = 18)
    title = 'Sale Price Sorted by Sale Type'
    plt.title(title, fontsize = 22)
    datatable = plt.table(cellText = list(zip(
        tab[saletypeorder_premerge].index,
        tab[saletypeorder_premerge].values)),
                          colLabels = ['SaleType','Count'],
                          rowLabels = ['     '] * len(tab),
                          cellLoc = 'right', rowLoc = 'center',
                          loc = 'right',bbox = [0.7,.57,.3,.4])

    datatable.auto_set_font_size(False)
    datatable.set_fontsize(14)

    # set background and text colour of row headers
    for i in range(1,len(tab)+1):
        # set current cell to row header
        c = datatable.get_celld()[(i, -1)]
        c.set_color(pal[i-1])
        c.set_text_props(fontsize = 10,
                         horizontalalignment='left')

    fig.tight_layout()

    filename = 'SaleTypePreMerge' + 'SalePriceBoxPlot.svg'
    plt.savefig(filename, format='svg')


# remap the data, and regenerate the graph
saletype_map = {
    'WD '   : 'WD',
    'CWD'   : 'WD',
    'VWD'   : 'WD',
    'New'   : 'New',
    'COD'   : 'Other',
    'Con'   : 'Con',
    'ConLw' : 'Con',
    'ConLI' : 'Con',
    'ConLD' : 'Con',
    'Oth'   : 'Other'
}

remap(fulldatadf,
      'SaleType',
      saletype_map,
      'str')

saletypeorder_postmerge = ['WD',
                           'New',
                           'Con',
                           'Other']
if generatesaletypegraph:
    plt.rc('xtick', labelsize = axislabelssize)
    plt.rc('ytick', labelsize = axislabelssize)

    fig, ax = plt.subplots()
    plt.figure(figsize=(12,8))

    tab = fulldatadf['SaleType'].value_counts()

    # set color palette
    pal = sns.color_palette('Set2', len(tab))

    ax = sns.boxplot(x='SaleType',
                     y='SalePrice',
                     data=fulldatadf,
                     order = tab[saletypeorder_postmerge].index,
                     palette = pal)

    plt.xlabel('Sale Type', fontsize = 18)
    plt.ylabel('Sale Price', fontsize = 18)
    title = 'Sale Price Sorted by House Style'
    plt.title(title, fontsize = 22)
    datatable = plt.table(cellText = list(zip(
        tab[saletypeorder_postmerge].index,
        tab[saletypeorder_postmerge].values)),
                          colLabels = ['SaleType','Count'],
                          rowLabels = ['     '] * len(tab),
                          cellLoc = 'right', rowLoc = 'center',
                          loc = 'right',bbox = [0.7,.62,.3,.35])

    datatable.auto_set_font_size(False)
    datatable.set_fontsize(14)

    # set background and text colour of row headers
    for i in range(1,len(tab)+1):
        # set current cell to row header
        c = datatable.get_celld()[(i, -1)]
        c.set_color(pal[i-1])
        c.set_text_props(fontsize = 10,
                         horizontalalignment='left')

    fig.tight_layout()

    filename = 'SaleTypePostMerge' + 'SalePriceBoxPlot.svg'
    plt.savefig(filename, format='svg')

##############################################################
#              Handle Condition1 / Condition2                #
##############################################################

from cleaning import checkIfIn

# define variables for different conditions
railroadadj = ['RRAn', 'RRAe']    # RRAdj
railroadbes = ['RRNn', 'RRNe']    # RRNear
roadadj     = ['Artery', 'Feedr'] # RoadAdj
posnear     = ['PosN', 'PosA']    # PosNear

fulldatadf['RRAdj'] = fulldatadf.apply(
    lambda x: checkIfIn(
        [x['Condition1'],
           x['Condition2']],
         railroadadj),
    axis = 1)

fulldatadf['RRNear'] = fulldatadf.apply(
    lambda x: checkIfIn(
        [x['Condition1'],
         x['Condition2']],
        railroadbes),
    axis=1)

fulldatadf['RoadAdj'] = fulldatadf.apply(
    lambda x: checkIfIn(
        [x['Condition1'],
         x['Condition2']],
        roadadj),
    axis=1)

fulldatadf['PosNear'] = fulldatadf.apply(
    lambda x: checkIfIn(
        [x['Condition1'],
         x['Condition2']],
        posnear),
    axis=1)

# now that we have rearranged the data,
# we can drop these columns
dropIrrelevantColumns(fulldatadf,
                      ['Condition1',
                       'Condition2'])

##############################################################
#                     HANDLE MSSUBCLASS                      #
##############################################################

# MSSubClass needs graphs generated to visualize

# list of MSSubClass levels with PUD in description
PUD_list = [120, 150, 160, 180]
nonPUD_list = [20, 45, 50, 60, 80, 85]

# create 'isPUD' column in fulldatadf
fulldatadf['isPUD'] = fulldatadf['MSSubClass'].apply(
    lambda x: 1 if x in PUD_list else 0)

####################GRAPHING MSSUBCLASS#######################

# create new dataframe only with these levels for MSSubClass
PUD_mask = fulldatadf['MSSubClass'].isin(PUD_list + nonPUD_list)
subclassdf = pd.DataFrame(fulldatadf[PUD_mask])

# specify the order for visualization purposes
subclass_order = ['1Story',
                  '1StoryPUD',
                  '1 1/2Story',
                  '1 1/2StoryPUD',
                  '2Story',
                  '2StoryPUD',
                  'Multilevel',
                  'MultilevelPUD']

# specify the labels (add new lines)
subclass_labels = ['1Story',
                   '1Story\nPUD',
                   '1 1/2Story',
                   '1 1/2Story\nPUD',
                   '2Story',
                   '2Story\nPUD',
                   'Multilevel',
                   'Multilevel\nPUD']

# map for taking subclass from discrete numerical into
# nominal categorical for graphing purposes
subclass_map = {
        120 : '1StoryPUD',
        20  : '1Story',
        150 : '1 1/2StoryPUD',
        45  : '1 1/2Story',
        50  : '1 1/2Story',
        160 : '2StoryPUD',
        60  : '2Story',
        180 : 'MultilevelPUD',
        80  : 'Multilevel',
        85  : 'Multilevel'
        }

remap(subclassdf,
      'MSSubClass',
      subclass_map,
      'str')

# specify the type of graph to be generated,
# and parameters to be passed in
subclass_graphtype = 'bar' # either box or bar
axislabelssize = 14
pal = sns.color_palette("Paired", 8)

if subclass_graphtype == 'box':
    plt.rc('xtick', labelsize = axislabelssize)
    plt.rc('ytick', labelsize = axislabelssize)

    fig, ax = plt.subplots()
    plt.figure(figsize=(14,8))
    tab = subclassdf['MSSubClass'].value_counts()
    ax = sns.boxplot(x = 'MSSubClass',
                     y = 'SalePrice',
                     data = subclassdf,
                     order = subclass_order,
                     palette = pal
                     )

    # add table of counts to the graph
    datatable = plt.table(cellText = list(zip(
    tab[subclass_order].index,
    tab[subclass_order].values)),
                      colLabels = ['MSSubClass','Count'],
                      rowLabels = ['     '] * len(tab),
                      cellLoc = 'right',
                      rowLoc = 'center',
                      loc = 'right',
                      bbox = [0.7,.62,.3,.35])

    # # set background and text colour of row headers
    for i in range(1,len(tab)+1):
        # set current cell to row header
        c = datatable.get_celld()[(i, -1)]
        c.set_color(pal[i-1])
        c.set_text_props(fontsize = 14,
                         horizontalalignment='left')

    datatable.auto_set_font_size(False)
    datatable.set_fontsize(14)

    locs, labels = plt.xticks()

    plt.xticks(ticks = locs,
           labels = subclass_labels)

    plt.xlabel('MSSubClasses', fontsize = 18)
    plt.ylabel('SalePrice', fontsize = 18)
    plt.title('Sale Price of PUD vs non PUD Homes', fontsize = 22)

    fig.tight_layout()

    plt.savefig('PUDMSSubclassSalePriceBox.svg', format = 'svg')

if subclass_graphtype == 'bar':
    plt.rc('xtick', labelsize = axislabelssize)
    plt.rc('ytick', labelsize = axislabelssize)

    fig, ax = plt.subplots()
    plt.figure(figsize=(14,8))
    tab = subclassdf['MSSubClass'].value_counts()
    ax = sns.barplot(x = 'MSSubClass',
                     y = 'SalePrice',
                     data = subclassdf,
                     order = subclass_order,
                     palette = pal
                     )

    locs, labels = plt.xticks()
    plt.xticks(ticks = locs,
               labels = subclass_labels)

    plt.xlabel('MSSubClasses', fontsize = 18)
    plt.ylabel('SalePrice', fontsize = 18)
    plt.title('Sale Price of PUD vs non PUD Homes', fontsize = 22)

    fig.tight_layout()

    plt.savefig('PUDMSSubclassSalePriceBar.svg', format = 'svg')

# now that we have used MSSubClass to filter
# PUD / non-PUD homes, the column can be dropped
# due to redunant information
dropIrrelevantColumns(fulldatadf,
                      'MSSubClass')


##############################################################
#                   HANDLE HOUSINGSTYLE                      #
##############################################################

# Here, I want to merge finished and unfinished
# 1.5, 2.5 and split level homes, but first we need to
# visualize the data

# specify if graphs should be generated
generatehousestylegraphs = False

housestyleorder_premerge = ['1Story',
                            '1.5Unf',
                            '1.5Fin',
                            '2Story',
                            '2.5Unf',
                            '2.5Fin',
                            'SLvl',
                            'SFoyer']

if generatehousestylegraphs:
    plt.rc('xtick', labelsize = axislabelssize)
    plt.rc('ytick', labelsize = axislabelssize)

    fig, ax = plt.subplots()
    plt.figure(figsize=(12,8))

    tab = fulldatadf['HouseStyle'].value_counts()

    # set color palette
    pal = sns.color_palette('Set2', len(tab))

    ax = sns.boxplot(x='HouseStyle',
                     y='SalePrice',
                     data=fulldatadf,
                     order = tab[housestyleorder_premerge].index,
                     palette = pal)

    plt.xlabel('House Style', fontsize = 18)
    plt.ylabel('Sale Price', fontsize = 18)
    title = 'Sale Price Sorted by House Style'
    plt.title(title, fontsize = 22)
    datatable = plt.table(cellText = list(zip(
        tab[housestyleorder_premerge].index,
        tab[housestyleorder_premerge].values)),
                          colLabels = ['HouseStyle','Count'],
                          rowLabels = ['     '] * len(tab),
                          cellLoc = 'right', rowLoc = 'center',
                          loc = 'right',bbox = [0.7,.62,.3,.35])

    datatable.auto_set_font_size(False)
    datatable.set_fontsize(14)

    # set background and text colour of row headers
    for i in range(1,len(tab)+1):
        # set current cell to row header
        c = datatable.get_celld()[(i, -1)]
        c.set_color(pal[i-1])
        c.set_text_props(fontsize = 10,
                         horizontalalignment='left')

    fig.tight_layout()

    filename = 'HouseStylePreMerge' + 'SalePriceBoxPlot.svg'
    plt.savefig(filename, format='svg')

# remap the data, and regenerate the graph
housestyle_map = {
        '1Story' : '1Story',
        '2Story' : '2Story',
        '1.5Fin' : '1.5Story',
        '1.5Unf' : '1.5Story',
        '2.5Fin' : '2.5Story',
        '2.5Unf' : '2.5Story',
        'SLvl'   : 'Split',
        'SFoyer' : 'Split'
        }

remap(fulldatadf,
      'HouseStyle',
      housestyle_map,
      'str')

housestyleorder_postmerge = ['1Story',
                             '1.5Story',
                             '2Story',
                             '2.5Story',
                             'Split']
if generatehousestylegraphs:
    plt.rc('xtick', labelsize = axislabelssize)
    plt.rc('ytick', labelsize = axislabelssize)

    fig, ax = plt.subplots()
    plt.figure(figsize=(12,8))

    tab = fulldatadf['HouseStyle'].value_counts()

    # set color palette
    pal = sns.color_palette('Set2', len(tab))

    ax = sns.boxplot(x='HouseStyle',
                     y='SalePrice',
                     data=fulldatadf,
                     order = tab[housestyleorder_postmerge].index,
                     palette = pal)

    plt.xlabel('House Style', fontsize = 18)
    plt.ylabel('Sale Price', fontsize = 18)
    title = 'Sale Price Sorted by House Style'
    plt.title(title, fontsize = 22)
    datatable = plt.table(cellText = list(zip(
        tab[housestyleorder_postmerge].index,
        tab[housestyleorder_postmerge].values)),
                          colLabels = ['HouseStyle','Count'],
                          rowLabels = ['     '] * len(tab),
                          cellLoc = 'right', rowLoc = 'center',
                          loc = 'right',bbox = [0.7,.62,.3,.35])

    datatable.auto_set_font_size(False)
    datatable.set_fontsize(14)

    # set background and text colour of row headers
    for i in range(1,len(tab)+1):
        # set current cell to row header
        c = datatable.get_celld()[(i, -1)]
        c.set_color(pal[i-1])
        c.set_text_props(fontsize = 10,
                         horizontalalignment='left')

    fig.tight_layout()

    filename = 'HouseStylePostMerge' + 'SalePriceBoxPlot.svg'
    plt.savefig(filename, format='svg')

##############################################################
#                        SALE CONDITION                      #
##############################################################
generatesaleconditiongraphs = True
if generatehousestylegraphs:
    plt.rc('xtick', labelsize = axislabelssize)
    plt.rc('ytick', labelsize = axislabelssize)

    fig, ax = plt.subplots()
    plt.figure(figsize=(12,8))

    tab = fulldatadf['SaleCondition'].value_counts()

    # set color palette
    pal = sns.color_palette('Set2', len(tab))

    ax = sns.boxplot(x='SaleCondition',
                     y='SalePrice',
                     data=fulldatadf,
                     order = tab[housestyleorder_premerge].index,
                     palette = pal)

    plt.xlabel('Sale Condition', fontsize = 18)
    plt.ylabel('Sale Price', fontsize = 18)
    title = 'Sale Price Sorted by Sale Condition'
    plt.title(title, fontsize = 22)
    datatable = plt.table(cellText = list(zip(
        tab[housestyleorder_premerge].index,
        tab[housestyleorder_premerge].values)),
                          colLabels = ['SaleCondition','Count'],
                          rowLabels = ['     '] * len(tab),
                          cellLoc = 'right', rowLoc = 'center',
                          loc = 'right',bbox = [0.7,.62,.3,.35])

    datatable.auto_set_font_size(False)
    datatable.set_fontsize(14)

    # set background and text colour of row headers
    for i in range(1,len(tab)+1):
        # set current cell to row header
        c = datatable.get_celld()[(i, -1)]
        c.set_color(pal[i-1])
        c.set_text_props(fontsize = 10,
                         horizontalalignment='left')

    fig.tight_layout()

    filename = 'SaleCondition' + 'SalePriceBoxPlot.svg'
    plt.savefig(filename, format='svg')

# filter 'SaleCondition' by including
# Normal and Partial sales only
salecondition_cols = ['Normal', 'Partial']

salecondition_mask = fulldatadf['SaleCondition'].isin(salecondition_cols)

fulldatadf = fulldatadf[salecondition_mask]
