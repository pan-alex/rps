import numpy as np
import pandas as pd
# from sklearn.tree import DecisionTreeClassifier
from sklearn import model_selection
import xgboost as xgb
import matplotlib.pyplot as plt
import os
import pickle


# Where I have graphviz saved; needed to visualize xgb trees
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

rps_data = pd.read_csv('data/intermediate/rps_data_12_past_moves.csv')

# Since many of the RPS games in the data are only 1 round (where there are no
# actual predictors available other than the "average" move) these would likely
# just adding noise to the model.
# To ensure the model has at least two predictors ('minus1' and 'outcome'), I
# will filter the data to only include games that at least go to round 2.
rps_data = rps_data.dropna(subset=['minus1'])

# features = ['minus1', 'minus2', 'minus3', 'minus4', 'minus5', 'minus6',
#             'minus7', 'minus8', 'minus10', 'minus11', 'minus12',
#             'won_minus1', 'won_minus2', 'won_minus3', 'won_minus4', 'won_minus5',
#             'won_minus6', 'won_minus7', 'won_minus8', 'won_minus9', 'won_minus10',
#             'won_minus11', 'won_minus12']

features = ['minus1', 'minus2', 'minus3', 'won_minus1', 'won_minus2', 'won_minus3']
# features = ['minus1']

# Some minor recoding of variables
# xgboost requires classes start w/ 0 so R, P, S is converted to 0, 1, 2
throw, labels = pd.factorize(rps_data['throw'])

rps_dummies = pd.get_dummies(rps_data[features])

x_train, x_test, y_train, y_test = model_selection.train_test_split(
        rps_dummies, throw, test_size=0.2, random_state=1)

#
# clf = xgb.XGBClassifier(seed=1).fit(
#         x_train, y_train, eval_set=[(x_train, y_train), (x_test, y_test)])

dtrain = xgb.DMatrix(x_train, label=y_train)
dtest = xgb.DMatrix(x_test, label=y_test)

param = {'max.depth': 2,'objective': 'multi:softprob', 'num_class': 3, 'verbosity': 2}
model = xgb.XGBClassifier(kwargs = param)
model.fit(x_train, y_train)


# # Test predictions vs. training data; random chance = 0.33
# y_pred = model.predict(x_train)
# pd.Series(y_pred == y_train).value_counts()
# (y_pred == y_train).mean()
#
# # Test predictions vs. test set
# y_test_pred = model.predict(x_test)
# pd.Series(y_test_pred == y_test).value_counts()
# (y_test_pred == y_test).mean()
#
# pd.Series(y_test_pred).value_counts()

# bst.get_score(importance_type='gain')
with open('source/data/xgb_model.pkl', 'wb') as f:
    pickle.dump(model, f)