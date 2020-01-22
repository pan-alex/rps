import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential, model_from_json
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt

X = np.load('data/final/lstm_X.npy')
Y = np.load('data/final/lstm_Y.npy')

# Generate data for keras
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=1)

# Define RNN shape parameters
batch_size = None    # unspecified training mini-batch size; let Keras handle
T_x = 12    # Number of time steps to include
n_x = 3    # Length of x at each time step (i.e., vocab size)



#################################### Model 1

# Define model architecture
model = Sequential()
model.add(LSTM(units=40, batch_input_shape=(None, T_x, n_x), return_sequences=True,
               dropout=0.25, recurrent_dropout=0.25))
model.add(LSTM(units=40, batch_input_shape=(None, T_x, n_x), return_sequences=False,
               dropout=0.25, recurrent_dropout=0.25))
model.add(Dense(3, activation='softmax'))

# Initialize model (note model can be trained continuously as long as it is not re-initialized)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])
model.fit(x_train, y_train, epochs=40, validation_data=(x_test, y_test), shuffle=False, verbose=2)

# Assess model
plt.plot(model.history.history['loss'])

results = model.predict(x_test)
from source.learning.model_assessment_utils import *

# 1. Assess categorical accuracy
# A random guesser would have an error of 0.333
categorical_accuracy(results, y_test)

# 2. Assess expected value
# If a win is 1, a loss is -1, and a loss is 0, a random guesser would have an EV = 0
outcomes = expected_value(results, y_test)
pd.Series(outcomes).value_counts()
np.sum(outcomes)


# Save the model; Trained on 50 epochs so far
with open('source/learning/lstm_model.pkl', 'wb') as f:
    import pickle
    pickle.dump(model, f)




#################################### Model 2



# Define model architecture
model2 = Sequential()
model2.add(LSTM(units=2, batch_input_shape=(None, T_x, n_x), return_sequences=False,
               dropout=0.5, recurrent_dropout=0))
model2.add(Dense(3, activation='softmax'))

# Initialize model2 (note model can be trained continuously as long as it is not re-initialized)
model2.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])
model2.fit(x_train, y_train, epochs=200, validation_data=(x_test, y_test), shuffle=False, verbose=2)

# Assess the model:
plt.plot(model2.history.history['loss'])    # After 50 - 100 epochs the change in loss is negligible.
results = model2.predict(x_test)

# 1. Assess categorical accuracy
# A random guesser would have an error of 0.333
categorical_accuracy(results, y_test)

# 2. Assess expected value
# If a win is 1, a loss is -1, and a loss is 0, a random guesser would have an EV = 0
outcomes = expected_value(results, y_test)
pd.Series(outcomes).value_counts()
np.sum(outcomes)



# Save the model
# with open('source/learning/lstm_model2.pkl', 'wb') as f:
#     import pickle
#     pickle.dump(model2, f)






###
#### Save and load model
###
# # serialize model to JSON
# model_json = model.to_json()
# with open("source/learning/lstm_model2.json", "w") as json_file:
#     json_file.write(model_json)
# model.save_weights("source/learning/lstm_model2.h5")
#
# # load json and create model
# with open('source/learning/lstm_model1.json', 'r') as json_file:
#     loaded_model_json = json_file.read()
# loaded_model = model_from_json(loaded_model_json)
# loaded_model.load_weights("source/learning/lstm_model1.h5")
