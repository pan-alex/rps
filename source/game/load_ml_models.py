from source.game.rps_game import *
import numpy as np
import pandas as pd
import pickle
import xgboost as xgb

with open('source/data/xgb_model.pkl', 'rb') as f:
    model_xgboost = pickle.load(f)

def make_prediction_xgboost(model, input1, outcomes):
    # features must be listed this way to match the order that the xgboost model expects.
    # However, this is the opposite order of how the game inputs are recorded
    # (where data from more recent games appears at the end of the list)
    # Therefore we slice the list to retrieve the last 3 items of `input1` and
    # `outcomes` and then reverse them via [::-1] to match the order of the features.
    # This matches the correct list elements to the correct variable, and keeps the
    # variables in the order that the xgboost model expects.
    features_input = ['minus1', 'minus2', 'minus3',]
    features_outcomes = ['won_minus1', 'won_minus2', 'won_minus3']

    # Recode input1 to match model inputs
    input1 = pd.Series(input1[-3:][::-1], index = features_input)  # Last 3 rounds
    outcomes = pd.Series(outcomes[-3:][::-1], index = features_outcomes)
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

#
# input1 = [1, 1, 1]
# outcomes = [-1, -1, -1]
# make_prediction_xgboost(model_xgboost, input1, outcomes)



# Notes
# - Gets stuck in a loop if player goes only scissors (alternates rock + scissors)
# - Gets stuck in a loop if player goes only rock (always rock)
# - Loop if always scissors(alternates rock + paper)
# - Rock/paper alternating wins most times