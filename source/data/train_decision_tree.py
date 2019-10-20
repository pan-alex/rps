import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import model_selection
import xgboost as xgb
import matplotlib.pyplot as plt
import os

# Where I have graphviz saved; needed to visualize xgb trees
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

rps_data = pd.read_csv('data/intermediate/rps_data_12_past_moves.csv')
# features = ['minus1', 'minus2', 'minus3', 'minus4', 'minus5', 'minus6',
#             'minus7', 'minus8', 'minus10', 'minus11', 'minus12',
#             'won_minus1', 'won_minus2', 'won_minus3', 'won_minus4', 'won_minus5',
#             'won_minus6', 'won_minus7', 'won_minus8', 'won_minus9', 'won_minus10',
#             'won_minus11', 'won_minus12']

features = ['minus1', 'minus2', 'minus3', 'won_minus1', 'won_minus2', 'won_minus3']

# Some minor recoding of variables
throw, labels = pd.factorize(rps_data['throw'])  # xgboost requires classes start w/ 0

rps_dummies = pd.get_dummies(rps_data[features])

x_train, x_test, y_train, y_test = model_selection.train_test_split(
        rps_dummies, throw, test_size=0.2, random_state=1)

#
# clf = xgb.XGBClassifier(seed=1).fit(
#         x_train, y_train, eval_set=[(x_train, y_train), (x_test, y_test)])

dtrain = xgb.DMatrix(x_train, label=y_train)
dtest = xgb.DMatrix(x_test, label=y_test)

param = {'max.depth': 2,'objective': 'multi:softmax', 'num_class': 3, 'verbosity': 2}
model = xgb.XGBClassifier(kwargs = param)
model.fit(x_train, y_train)

y_pred = model.predict(x_train)
pd.Series(y_pred == y_train).value_counts()
(y_pred == y_train).mean()

y_test_pred = model.predict(x_test)
pd.Series(y_test_pred == y_test).value_counts()
(y_test_pred == y_test).mean()


# bst.dump_model('test.txt')


# fig, ax = plt.subplots(figsize=(100, 100))
# gr = xgb.plot_tree(bst, num_trees=0, ax=ax, rankdir='LR')
# plt.savefig('test.pdf')
# plt.show()
# preds = clf.predict(y_test)

bst.get_score(importance_type='gain')
