# -*- coding: utf-8 -*-
"""
Created on Mon May  1 05:38:04 2017

@author: mw352
"""

import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, TimeDistributed, Flatten
from keras.layers import LSTM

from keras.layers import Conv1D, MaxPooling2D

# Input sequence
X_test = np.loadtxt("D:\\tandon\\AI_for_game\\osu_project\\normed_training_input.csv",delimiter=",",skiprows=0)

Y_test = np.loadtxt("D:\\tandon\\AI_for_game\\osu_project\\normed_training_output.csv",delimiter=",",skiprows=0)


# Preprocess Data:
X_test = np.array(X_test, dtype=float) # Convert to NP array.

# target = wholeSequence[0:2] 
Y_test = np.array(Y_test, dtype=float)

N = int(X_test.shape[0] / 120)


X_test = X_test.reshape((N, 120, 15))
Y_test = Y_test.reshape((N, 120, 3))

#build lstm model
model = Sequential()
model.add(LSTM(64, input_shape=(120,15),activation='tanh', recurrent_activation='relu',
                            use_bias=True, kernel_initializer='glorot_uniform',
                            recurrent_initializer='orthogonal', bias_initializer='zeros',
                            unit_forget_bias=True, 
                            return_sequences=True))

model.add(LSTM(64,return_sequences=True, activation='relu'))
#model.add(LSTM(32,input_length = 24000, input_dim=3,return_sequences=True))
model.add(Dense(64, activation='relu'))
model.add(Dense(3, activation='sigmoid'))
#model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

#model.fit(X_test, Y_test, epochs=13, batch_size=64, verbose=1)
#model.save('D:\\tandon\\AI_for_game\\osu_project\\refined_my_model_second .h5')

'''
X_target = X_test[0:50]
predict = model.predict(X_target, verbose = 1)
print (predict)
np.savetxt('D:\\tandon\\AI_for_game\\osu_project\\normed_training_result.csv', predict, delimiter = ',') 
model.save('D:\\tandon\\AI_for_game\\osu_project\\my_model.h5')
model2 = model.load('D:\\tandon\\AI_for_game\\osu_project\\my_model.h5')
'''
'''
print("data",data)
print("target",target)
# Reshape training data for Keras LSTM model
# The training data needs to be (batchIndex, timeStepIndex, dimentionIndex)
# Single batch, 9 time steps, 11 dimentions
data = data.reshape((2, 4, 11))
target = target.reshape((2, 4))
print("data",data)
print("target",target)

# Build Model
model = Sequential() 
# model.add(Conv1D(11, kernel_size=2,
#                  activation='relu',
#                  input_shape=(2, 4, 11)))
# model.add(Flatten())

model.add(LSTM(11, input_shape=(4, 11), unroll=True, return_sequences=True))
model.add(LSTM(11, input_shape=(4, 11), unroll=True, return_sequences=False))
model.add(Dense(4))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(data, target, epochs=10, batch_size=1, verbose=1)
'''