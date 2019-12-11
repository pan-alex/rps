from source.game.rps_game import *
import numpy as np
import pandas as pd
import pickle
import xgboost as xgb

with open('source/data/xgb_model.pkl', 'rb') as f:
    model_xgboost = pickle.load(f)

def make_prediction_xgboost(model, input1, outcomes):
    features = ['minus1', 'minus2', 'minus3', 'won_minus1', 'won_minus2', 'won_minus3']

    # Recode input1 to match model inputs
    input1 = pd.Series(input1[-3:], index = features[0:3])   # Last 3 rounds
    outcomes = pd.Series(outcomes[-3:], index = features[3:])
    input1_to_y = {1:0, 2:1, 3:2}
    y = input1.replace(input1_to_y)

    # Map input1 and outcomes to a dataframe, then map to an XGboost matrix
    row = y.append(outcomes)
    df = pd.DataFrame([row])
    df = pd.get_dummies(df)
    dtest = xgb.DMatrix(df)

    # Predict, choose what beats the prediction, and translate back to 'R', 'P', or 'S'
    model_pred = int(model.predict(df))
    # 0 = R, so throw P (2); 1 = P, so throw S (3), 2 = S, so throw R (1)
    model_pred_to_throw = {0:2, 1:3, 2:1}
    throw = model_pred_to_throw[model_pred]

    return throw

input1 = [1, 2, 3, 1, 2, 3]
outcomes = [1, 1, 0, -1, -1, 0]

input1 = [3, 3, 3]
outcomes = [0, 0, 0]
make_prediction_xgboost(model_xgboost, input1, outcomes)