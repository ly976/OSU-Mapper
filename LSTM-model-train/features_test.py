# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 23:04:54 2017

@author: mw352
"""

# We'll need numpy for some mathematical operations
import numpy as np

# Librosa for audio
import librosa
# And the display module for visualization
import librosa.display

#audio_path = librosa.util.example_audio_file()

# or uncomment the line below and point it at your favorite song:
#
#audio_path = 'Data/test.wav'
audio_path = "D:/Program Files/osu!/Songs/13019 Daisuke Achiwa - BASARA/BASARA.mp3"

y, sr = librosa.load(audio_path)
mfcc = librosa.feature.mfcc(y=y, sr=sr,n_mfcc = 1)
'''
# Let's make and display a mel-scaled power (energy-squared) spectrogram
S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)

# Convert to log scale (dB). We'll use the peak power as reference.
log_S = librosa.logamplitude(S, ref_power=np.max)

# Next, we'll extract the top 13 Mel-frequency cepstral coefficients (MFCCs)
mfcc        = librosa.feature.mfcc(S=log_S)

# Let's pad on the first and second deltas while we're at it
delta_mfcc  = librosa.feature.delta(mfcc)
delta2_mfcc = librosa.feature.delta(mfcc, order=2)
'''
print(mfcc)
np.mean(mfcc)
print(len(mfcc[0]))