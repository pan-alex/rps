"""
Script to clean and prepare data for training.
Reads in CSV data in tabular format and outputs ML-ready numpy arrays (with the exception
of test-train splitting)
"""
import numpy as np
import pandas as pd

def one_hot_encode(input, nb_classes=3):
    '''
    Based off https://stackoverflow.com/questions/38592324/one-hot-encoding-using-numpy#38592416
    '''
    input = input.astype(int)   # Must be an integer to use as index
    # RPS inputs are R=1, P=2, S=3, and missing = 0. Therefore shift all inputs
    # down by 1 so that R = 0, P = 1, S = 2, missing = -1 (i.e., last row)
    input_to_index = input.astype(int) - 1
    # 3 is the # of possible inputs; 4 rows (with 1 row of all 0s for missing values)
    one_hot_encoded_array = np.eye(N=nb_classes+1, M=nb_classes)[input_to_index]
    return one_hot_encoded_array


rps = pd.read_csv('data/intermediate/rps_data_sequence.csv')
rps = rps.fillna(0)    # Fill NaNs with 0.

# Extract the throw column, which will be the ground-truth labels for the prediction
Y = one_hot_encode(np.array(rps.throw))

# Extract the remaining columns.
# Reverse the order of the array so that the last element is the most recent throw.
rps_X = rps.drop(['throw'], axis=1)
rps_X = rps_X[rps_X.columns[::-1]]

# Convert the remaining columns to one-hot-encoded arrays. Sequences are zero-padded for missing values.
X = one_hot_encode(rps_X)

### Some tests to compare that the results are correct
# rps_X.iloc[201]
# X[201]
# rps_X.iloc[20001]
# X[20001]
###

np.save('data/final/lstm_X.npy', X)
np.save('data/final/lstm_Y.npy', Y)
