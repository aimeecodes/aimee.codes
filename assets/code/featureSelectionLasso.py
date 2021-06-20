#######################################################
#                                                     #
#            2021-06-14 blog post script              #
#                                                     #
#######################################################

# this script covers Method 3: LASSO of June's blog post
# about feature selection.

# import tools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import multiprocessing as mp

from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline

from group_lasso import GroupLasso
from group_lasso.utils import extract_ohe_groups

GroupLasso.LOG_LOSSES = True

import scipy.sparse

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.inspection import permutation_importance
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import time

# read in the datasets
train_data_path = '../cleaned-data/cleaned_ihd_train.csv'
test_data_path = '../cleaned-data/cleaned_ihd_test.csv'

train_data = pd.read_csv(train_data_path)
test_data = pd.read_csv(test_data_path)

# drop unneccessary columns from the datasets
train_data = train_data.drop('Unnamed: 0', axis=1)
train_data = train_data.drop('Id', axis=1)

test_data = test_data.drop('Unnamed: 0', axis=1)
test_data = test_data.drop('Id', axis=1)

# specify X as features and Y as target variable
X = train_data.drop('SalePrice', axis=1)
Y = train_data['SalePrice']

# make list of categorical and numerical features
isCat = X.dtypes == 'object'
cat_feat = list(X.dtypes[isCat].index)
num_feat = list(X.dtypes[~isCat].index)

# save feature names in list
feature_names = list(X.columns)

# create train/cross validation splits
Xtrain, Xcv, Ytrain, Ycv = train_test_split(X, Y,
                                            test_size = 0.33,
                                            random_state=42)

# create categorical encoder
categorical_encoder = OneHotEncoder(handle_unknown='ignore')


# extract onehotencoded categorical variables into separate sparse scipy matrix
Xcat_ohe = categorical_encoder.fit_transform(X[cat_feat])

# get the groups data from this onehotencoded dataframe
groups = extract_ohe_groups(categorical_encoder)

# create new groups order
groups = np.hstack([groups, len(cat_feat) + np.arange(len(num_feat))])

# scale the numerical features
scaler = StandardScaler()
Xnum_sca = scaler.fit_transform(X[num_feat], Y)

# put the scaled numerical features and ohe'd
# categorical features back together
# (in a sparse scipy array format)
X_grouped = scipy.sparse.hstack(
    [Xcat_ohe,
     scipy.sparse.csr_matrix(Xnum_sca)])

# keeps track of the order of variable names once
# categorical and numerical features are glued back together
# post-processing
feature_order = cat_feat + num_feat

grpLasso = GroupLasso(
    groups = groups,
    group_reg = 10,
    l1_reg = 0,
    scale_reg = 'inverse_group_size',
    supress_warning = True,
    n_iter = 10000,
    frobenius_lipschitz = True)

start_time = time.time()
grpLasso.fit(X_grouped,Y)
elapsed_time = time.time() - start_time

print(f"time wasted: {elapsed_time}")

Yhat = grpLasso.predict(X_grouped)

r2score = r2_score(Y, Yhat)
print(f"r2score: {r2score}")
print(grpLasso.chosen_groups_)
print(f"number of chosen groups: {len(grpLasso.chosen_groups_)}")

# make list of chosen groups (default format is set)
chosen_groups = list(grpLasso.chosen_groups_)

# make boolean list for is / is not in of
# length number of overall features (num and cat)
chosenbool = [False] * len(feature_order)

for i in range(len(chosen_groups)):
    chosenbool[chosen_groups[i]] = True

# get list of features that are filtered
selected_features = [i for (i, v) in zip(feature_order, chosenbool) if v]
discarded_features = [i for (i, v) in zip(feature_order, chosenbool) if not v]

print(f"discarded features: {discarded_features}")

# # create numerical handler
# # (handle unknowns by imputing the mean,
# # and scales numerical features)
# numerical_pipe = Pipeline([
#     ('imputer', SimpleImputer(strategy='mean')),
#      ('scaler', StandardScaler())])

# # create preprocessing transform step
# preprocessing = ColumnTransformer(
#     [('cat', categorical_encoder, cat_feat),
#      ('num', numerical_pipe, num_feat)])

# # create actual pipeline
# lasso = Pipeline([
#     ('preprocess', preprocessing),
#     ('variable_selection', GroupLasso(
#         groups = groups,
#         supress_warning = True)),
#     ('regressor', Lasso(alpha=(0.1)))])

# # train on Xtrain and Ytrain
# lasso.fit_transform(Xtrain, Ytrain)
