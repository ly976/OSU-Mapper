# -*- coding: utf-8 -*-
"""
Created on Sun May  7 15:10:07 2017

@author: mw352
"""

import numpy as np
import keras
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, TimeDistributed, Flatten
from keras.layers import LSTM
from keras.utils import plot_model
from keras.layers import Conv1D, MaxPooling2D

import pydot
import graphviz

model = load_model('D:\\tandon\\AI_for_game\\osu_project\\my_model.h5')
model.summary()
#pydot.find_graphviz = lambda: True
#plot_model(model, to_file='model.png')

'''
content = np.loadtxt("D:\\tandon\\AI_for_game\\osu_project\\dataset\\norm_data_basara\\norm_data\\BASARA.13019 Daisuke Achiwa - BASARA.trainable_all.v1.csv",delimiter=",",skiprows=0)

# Preprocess Data:
content = np.array(content, dtype=float) # Convert to NP array.

# target = wholeSequence[0:2] 
print(content.shape)
content.resize(12000, 18)
X_test = content[:,0:-3]


X_test = X_test.reshape((50, 240, 15))

predict = model.predict(X_test, verbose = 1)
'''