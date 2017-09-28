import sys
import librosa
import argparse
import csv
import numpy as np

# get onset strength
def mis_onset_strenghth(o_env, mis):
    return [o_env[librosa.core.time_to_frames(e[1]/1000, sr=sr)[0]] for e in mis]


# get onset feature
def getOnset(y, sr):
    onset_result = librosa.onset.onset_detect(y=y, sr=sr, precise=True, units='time')
    onset_result = [[1000 * e] for e in onset_result]
    return onset_result
   

# extratc mfcc feature from librosa 
def getmfcc(y, sr, mis):
    # Let's make and display a mel-scaled power (energy-squared) spectrogram
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)

    # Convert to log scale (dB). We'll use the peak power as reference.
    log_S = librosa.logamplitude(S, ref_power=np.max)

    # Next, we'll extract the top 13 Mel-frequency cepstral coefficients (MFCCs)
    mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=12)
 
    mfcc = list(map(list, zip(*mfcc)))

    feature = [mfcc[librosa.core.time_to_frames(m[1]/1000, sr=sr)[0]] for m in mis]
    return feature



# get the index of closest number of x in list y
def closestindex(x, y):
    for i in range(len(y)):
        if y[i][1] == x:
            return i
        elif y[i][1] > x:
            if i == 0 or abs(y[i][1] - x) <= abs(y[i-1][1] - x):
                return i
            else:
                return i - 1
    if i == len(y) - 1:
        return i

# get is it onset for every mis using the extracted onset feature, 
def isonset(x, y):
    y_copy = [[] for i in range(len(y))]
    startindex = 0
    for i in range(len(x)):
        index = closestindex(x[i][0], y)
        if len(y_copy[index + startindex]) == 0:
            y_copy[index + startindex] = [1]
        startindex += index
        y = y[index:]
    for i in range(len(y_copy)):
        if len(y_copy[i]) == 0:
            y_copy[i] = [0]
    return y_copy

# get is it beat feature, every other 4 mis has a beat
def isbeat(mis):
    division = 4
    return [[1] if i % division == 0 else [0] for i in range(len(mis))]


# merge all the features in a matrix as training feature 
def merge(onset_strength, is_onset, beat, mfcc):
    feature = []
    for i in range(len(onset_strength)):
        feature.append(onset_strength[i] + is_onset[i] + beat[i] + mfcc[i])
    return feature

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise argparse.ArgumentTypeError('the number of argument has to be 3')
        exit(-1)

    y, sr = librosa.load(sys.argv[1], sr = None)
    o_env = librosa.onset.onset_strength(y, sr=sr)
    times = librosa.frames_to_time(np.arange(len(o_env)), sr=sr) 

    onset = getOnset(y, sr)

    with open(sys.argv[2], 'r') as my_file:
        csvreader = csv.reader(my_file)
        mis = list(csvreader)
    
    mis = [[int(ele[0]), float(ele[1])] for ele in mis]
    mfcc = getmfcc(y, sr, mis)
    onset_strength = [[o_env[librosa.core.time_to_frames(e[1]/1000, sr=sr)[0]]] for e in mis]
    is_onset = isonset(onset, mis)
    beat = isbeat(mis)
    tr_f = merge(onset_strength, is_onset, beat, mfcc)

    writer = csv.writer(sys.stdout)
    writer.writerows(tr_f)
    

    