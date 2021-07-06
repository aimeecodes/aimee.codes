# Cleaning data module

# for data exploration
import pandas as pd
from functools import reduce

# for data filtering
from scipy.stats import iqr

# for predictions
from numpy.polynomial import Polynomial
import numpy as np

# import CSV stored data as pandas df
def importCSVasDF(filepath):
    return pd.read_csv(filepath)

# change column names to remove white spaces between words
def removeWhiteSpaceFromColumns(df):
    df.columns = list(map(lambda x: x.replace(" ", ""), list(df.columns)))

# combine importCSVasDF and removeWhiteSpaceFromColumns
def importCSVandRemoveWhiteSpace(filepath):
    df = importCSVasDF(filepath)
    removeWhiteSpaceFromColumns(df)
    return df

# drop irrelevant columns
def dropIrrelevantColumns(df, cols):
    df.drop(cols, axis = 1, inplace = True)

# fill categorical NAs with "None"
def fillCatNAwithNone(df, cols):
    for col in cols:
        df[col].fillna("None", inplace = True)

# fill numerical NAs with 0
def fillNumNAwithZero(df, cols):
    for col in cols:
        df[col].fillna(0, inplace = True)

# fill the NAs of a category with the mode of
# the category when grouped by another factor
def fillCatNAwithGroupedMode(df, colwithNAs, groupingcol):
    df[colwithNAs].fillna(
        df.groupby(groupingcol)[colwithNAs].transform(
            lambda x: x.mode().iloc[0]), inplace = True)

# run fillCatNAwithGroupedMode on a list of columns
# which have the same groupingcol
def fillCatNAwithGroupedModeList(df, listofcolswithNAs, groupingcol):
    for col in listofcolswithNAs:
        fillCatNAwithGroupedMode(df, col, groupingcol)

# fill the NAs of a category with the mode
# of the category
def fillCatNAwithMode(df, col):
    df[col].fillna(df[col].mode()[0], inplace = True)

# call fillCatNAwithMode on list of columns
def fillCatNAwithModeList(df, cols):
    for col in cols:
        fillCatNAwithMode(df, col)

# get IQR for a numeric column
def getIQR(df, col):
    return iqr(df[col])

# returns Q1 and Q3 for a numeric column
# as a list, where [0] is Q1, [1] is Q3
def getQ1Q3(df, col):
    return list(df[col].quantile([0.25, 0.75]))

# make filter for dataframe based on
# 1.5*IQR rule to filter outliers
def makeFilterIQRRule(df, col):
    iqr = getIQR(df, col)
    q1, q3 = getQ1Q3(df, col)
#     return [col, lambda x: x >= q1-1.5*iqr]    # this works
    return [col, lambda x: (x >= q1 - 1.5*iqr) & (x <= q3 + 1.5*iqr)]

# create a list of pairs, which define
# a numerical column, and a lambda function that will
# filter the column based on outliers
def makeIQROutlierPairs(df, cols):
    pairs = []

    for col in cols:
        pairs.append(makeFilterIQRRule(df, col))

    return pairs

# takes in a dataframe and numerical columns that need
# to be filtered based on 1.5*IQR, returns the dataframe without
#  samples w/ detected outliers
def removeIQROutliersFromDF(df,
                            cols):
    return filterFrame(
        df,
        makeFilters(df, makeIQROutlierPairs(df, cols)),
        list(df.columns))

# compute degree n polynomial model coefficients
# returns a list of n+1 items
def computeDegreeNPolyModelCoef(xdata, ydata, degree):
    return Polynomial.fit(xdata,
                          ydata,
                          degree).convert().coef

# produces filtered dataframe of columns in colnames
# df       > dataframe you want to filter
# colpreds > list of boolean
#            filters you want to apply using logical AND
# colnames > columns you want out of the filtered dataframe
def filterFrame(df, colpreds, colnames):
    return df[reduce(lambda x, y: x & y, colpreds)][colnames]

# returns list of levels within a factor
def getLevels(df, factor):
    return list(df[factor].value_counts().index)

# builds a dictionary of polynomial model coefficients for
# different factor1-levels (CATEGORICAL) to use factor2 (NUMERICAL)
# to make an estimate for factor3 (NUMERICAL)
# degree is the degree of polynomial for your model
def buildPolyModelsDict(df,
                        factor1,
                        factor2,
                        factor3,
                        pairs,
                        degree):

    # get list of levels from factor1
    levels = getLevels(df, factor1)

    # get column names from pairs, so that we can properly
    # pass the column names to filterFrame
    colnames = []

    for p in pairs:
        colnames.append(p[0])

    # initialize dictionary to return, where
    # keys   > levels of factor1,
    # values > lists of coefficients used to predict
    #        > factor3 from factor2
    coef_dict = {}

    for level in levels:
        # this guarantees the first filter is always separating out
        # all samples where factor1 == level
        filters = [df[factor1] == level] + makeFilters(df, pairs)

        data = filterFrame(df, filters, colnames)

        coef_dict[level] = computeDegreeNPolyModelCoef(
            data[factor2],
            data[factor3],
            degree)

    return coef_dict

# returns a list of dataframe predicates
# using partial booleans and column names
# requires list of pairs, where
# p[0]     > column name,
# p[1]     > partially applied boolean
# e.g.     > ['LotConfig', functools.partial(lambda y, x: x <= y, 80000)]
# multiple partial booleans can be applied to the same column,
# but there needs to be multiple pairs for each partial boolean
# e.g.     > ['LotConfig', functools.partial(lambda y, x: x >= y, 10000)]
def makeFilters(df, pairs):
    filters = []

    for p in pairs:
        filters.append(p[1](df[p[0]]))

    return filters

# takes in an array of polynomical coefficients and a point x,
# returns the value of the polynomial evaluated at x
# using numpy's polyval
def evaluatePolynomial(coef, x):
    return np.polyval(coef, x)

# takes in a dictionary of polynomial model coefficients, dataframe,
# and factor1 (CATEGORICAL), factor2 (NUMERICAL), and factor3 (NUMERICAL)
# factor1 has specific levels, factor2 is used to predict factor3
def predictAndFillNumericalNAsGroupedByCategory(df,
                                                coefdict,
                                                factor1,
                                                factor2,
                                                factor3):
    df[factor3].fillna(
        df.apply(lambda x: evaluatePolynomial(
            coefdict[x.loc[factor1]],
            x.loc[factor2]),
                 axis = 1),
        inplace = True)

# fill a discrete numerical variable (factor1) with the
# mode of it's related level when grouped by factor2
# factor1 is discrete numerical feature that is missing,
# factor2 is categorical feature w/ levels
def fillDiscreteNAwithMode(df, factor1, factor2):
    df[factor1].fillna(
        df.groupby(factor2)[factor1].transform(
            lambda x: x.mode().iloc[0]),
        inplace = True)

# fill a continuous numerical variable (factor1) with the
# mean of it's related level when grouped by factor2
# factor1 is continuous numerical feature that is missing,
# factor2 is categorical feature w/ levels
def fillContNAwithMean(df, factor1, factor2):
    df[factor1].fillna(
        df.groupby(factor2)[factor1].transform(
            lambda x: x.mean()),
        inplace = True)

# remaps some feature to another, default type is 'int'
# but if you're mapping to strings, must specify this
def remap(df, col, dictmap, dtype='int'):
    df[col] = df[col].map(dictmap).astype(dtype)

# given a list of columns, use the common dictmap
# to remap their ordinal features to discrete numerical
def remapCommonDict(df, cols, dictmap, dtype='int'):
    for col in cols:
        remap(df, col, dictmap, dtype)

# takes in 2 lists: checks if any members of list1 are
# members of list2
def checkIfIn(list1, list2):
    for item in list1:
        if item in list2:
            return True
    return False
