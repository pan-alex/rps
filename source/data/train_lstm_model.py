import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential, model_from_json
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt

###
#### Prepare Data
###
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

# Generate data for keras
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=1)


###
#### Build model
###
batch_size = None    # unspecified training mini-batch size; let Keras handle
T_x = 12    # Number of time steps to include
n_x = 3    # Length of x at each time step (i.e., vocab size)

# Define model architecture
model = Sequential()
model.add(LSTM(units=1, batch_input_shape=(None, T_x, n_x), return_sequences=False))
model.add(Dense(3, activation='softmax'))

# Initialize model (note model can be trained continuously as long as it is not re-initialized)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])

# Train the model
history = model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test), shuffle=False, verbose=2)


###
#### Assess model
###
# results = model.predict(x_test)
# plt.scatter(range(100), y_test[:100][0], c='r')
plt.plot(history.history['loss'])
plt.show()


###
#### Save and load model
###
# # serialize model to JSON
# model_json = model.to_json()
# with open("source/data/lstm_model1.json", "w") as json_file:
#     json_file.write(model_json)
# model.save_weights("source/data/lstm_model1.h5")
#
# # load json and create model
# with open('source/data/lstm_model1.json', 'r') as json_file:
#     loaded_model_json = json_file.read()
# loaded_model = model_from_json(loaded_model_json)
# loaded_model.load_weights("source/data/model.h5")
