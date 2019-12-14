from source.game.rps_game import *
import numpy as np
import pandas as pd
import pickle
import xgboost as xgb

with open('source/data/xgb_model.pkl', 'rb') as f:
    model_xgboost = pickle.load(f)

def make_prediction_xgboost(model, input1, outcomes):
    # features must be listed in a way that matches the order that the xgboost model expects.
    # However, this is the opposite order of how the game inputs are recorded
    # (where data from more recent games appears at the end of the list)
    features_input = ['minus1', 'minus2', 'minus3', 'minus4', 'minus5', 'minus6',
                      'minus7', 'minus8', 'minus10', 'minus11', 'minus12']
    features_outcomes = ['won_minus1', 'won_minus2', 'won_minus3', 'won_minus4', 'won_minus5', 'won_minus6',
                         'won_minus7', 'won_minus8', 'won_minus9', 'won_minus10', 'won_minus11', 'won_minus12']

    # Fill input1 and outcomes with empty values to the appropriate length
    # i.e., fill missing data with `None`
    input1 = input1 + [None]*(len(features_input) - len(input1))
    outcomes = outcomes + [None]*(len(features_outcomes)  - len(outcomes))

    # We reverse the inputs via [::-1] to match the order of the features and slice
    # them to retrieve the last X items of `input1` and `outcomes`. This matches
    # the correct list elements to the correct variable, and keeps the variables
    # in the order that the xgboost model expects.
    input1 = pd.Series(input1[::-1][:len(features_input)], index = features_input)  # Last 3 rounds
    outcomes = pd.Series(outcomes[::-1][:len(features_outcomes)], index = features_outcomes)
    input1_to_y = {1:0, 2:1, 3:2}    # Model treats Rock (1) as 0, etc.
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
