import numpy as np
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

# Define model architecture
model = Sequential()
model.add(LSTM(units=2, batch_input_shape=(None, T_x, n_x), return_sequences=False,
               dropout=0.25, recurrent_dropout=0.25))
model.add(Dense(3, activation='softmax'))

# Initialize model (note model can be trained continuously as long as it is not re-initialized)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])

# Train the model
history = model.fit(x_train, y_train, epochs=20, validation_data=(x_test, y_test), shuffle=False, verbose=2)


###
#### Assess model
###
# results = model.predict(x_test)
# plt.scatter(range(100), y_test[:100][0], c='r')
plt.plot(history.history['loss'])



###
#### Save and load model
###
# # serialize model to JSON
model_json = model.to_json()
with open("source/learning/lstm_model2.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("source/learning/lstm_model2.h5")

# # load json and create model
# with open('source/learning/lstm_model1.json', 'r') as json_file:
#     loaded_model_json = json_file.read()
# loaded_model = model_from_json(loaded_model_json)
# loaded_model.load_weights("source/learning/model.h5")