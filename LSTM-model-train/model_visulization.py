# -*- coding: utf-8 -*-
"""
Created on Mon May 15 14:49:29 2017

@author: mw352
"""
import keras
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import numpy
from keras.models import load_model

history = load_model('D:\\tandon\\AI_for_game\\osu_project\\my_model.h5')

# list all data in history
print(history.history)
#keras.callbacks.Callback(history)

'''
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
'''