import numpy as np
import math
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM, Activation


###
#### Read in data
###

# Exclude the first line, which contains headings
rps_as_array = np.genfromtxt('data/intermediate/rps_data_sequence.csv', delimiter=',')[1:]

# Reverse the order of the array, so that the last element is the most recent throw
rps_as_array_rev = np.flip(rps_as_array, axis=1)

# Remove nans; first we have to transform the data to a list, then filter nans
rps_as_array_rev_list = np.ndarray.tolist(rps_as_array_rev)

# Not clean and probably very inefficient but does the job...
n = len(rps_as_array_rev_list)
rps_clean =  [[] for _ in range(n)]
for i in range(n):
    rps_clean[i] = []
    for element in rps_as_array_rev_list[i]:
        if math.isnan(element) == False:
            rps_clean[i].append(element)

X = rps_clean

# Generate data for keras




###
#### Build Vocabulary
###
vocab = [1, 2, 3]
vocab_size = len(vocab)


###
#### Build model
###

#
model = Sequential()
model.add(LSTM(4, return_sequences=True))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])

