from source.game.rps_game import *
from source.data.process_lstm_data import one_hot_encode
import numpy as np
import pandas as pd
import pickle
import xgboost as xgb

# All models output an array of probabilities where element 0 is rock, element 1
# is paper, and element 2 is scissors.
model_pred_to_throw = {0: 2,  # 0 = R, so throw P (2)
                       1: 3,  # 1 = P, so throw S (3)
                       2: 1}  # 2 = S, so throw R (1)

###
#### Functions for the xgboost model
###
with open('source/learning/xgb_model.pkl', 'rb') as f:
    model_xgboost = pickle.load(f)

def make_prediction_xgboost(model, input1, outcomes):
    global model_pred_to_throw
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

    model_pred = int(model.predict(df))
    throw = model_pred_to_throw[model_pred]

    return throw

###
#### Functions for the LSTM model
###
with open('source/learning/lstm_model2_100epochs.pkl', 'rb') as f:
    model2_lstm = pickle.load(f)

def return_prediction_probabilities_lstm(model, input1):
    # Cut or zero-pad input1 to the last 12 moves.
    max_len = 12
    if len(input1) > max_len:
        input1_len = input1[-max_len:]
    else:
        input1_len =  [0]*(max_len - len(input1)) + input1

    # One-hot encode the input to be in the necessary format for the model.
    # Add an extra dimension to represent that the number of samples, m, is 1.
    x = one_hot_encode(np.array(input1_len))
    x = np.expand_dims(x, axis=0)    # shape is (1, 12, 3)

    prediction_probs = model2_lstm.predict(x)
    return prediction_probs.ravel()


def make_deterministic_prediction(prediction_probs):
    global model_pred_to_throw
    max_prob = np.argmax(prediction_probs)
    return model_pred_to_throw[max_prob]


def make_probabalistic_prediction(prediction_probs):
    global model_pred_to_throw
    random_choice = np.random.choice([0, 1, 2], p=prediction_probs.ravel())
    return model_pred_to_throw[random_choice]


def make_EV_prediction(prediction_probs):
    """
    Makes a prediction that maximizes expected value (wins = 1, ties = 0, losses = -1)
    """
    # same win_matrix as in rps_game except everything is shifted down since the model
    # is trying to predict what the opponent *would* play (and hence play whatever beats it)
    win_matrix = {2: {0: 0,
                      1: -1,
                      2: 1},
                  0: {0: 1,
                      1: 0,
                      2: -1},
                  1: {0: -1,
                      1: 1,
                      2: 0}
                  }
    expected_value = []
    # Calculate EV for each prediction. May not correspond to the prediction with
    # the highest probability (e.g., if rock is the most likely, but scissors is
    # also very likely, predicting scissors has higher EV than paper.
    for throw in range(3):
        expected_value.append(win_matrix[throw][0] * prediction_probs[0] +
                              win_matrix[throw][1] * prediction_probs[1] +
                              win_matrix[throw][2] * prediction_probs[2]
                              )
    max_ev = np.argmax(expected_value)
    return model_pred_to_throw[max_ev]


def make_prediction_lstm(model, input1, method='ev'):
    method = method.lower()
    prediction_probs = return_prediction_probabilities_lstm(model, input1)

    if method == 'ev' or method == 'expected value':
        throw = make_EV_prediction(prediction_probs)
    elif method == 'd' or method == 'deterministic':
        throw = make_deterministic_prediction(prediction_probs)
    elif method == 'p' or method == 'probabilistic':
        throw = make_probabalistic_prediction(prediction_probs)
    else:
        raise Exception('`method` must be "ev", "deterministic", or "probabilistic".')
    return throw





