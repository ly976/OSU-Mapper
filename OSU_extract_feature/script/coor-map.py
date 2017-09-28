import sys
import librosa
import argparse
import csv
import numpy as np
import os
import random
from coordinater_generater import generate_map_coordinate


# function merge is used for creating hit obejcts
def merge(mis, res, x_coor, y_coor):
    res = np.hstack([res, mis])
    mis = []
    # c is used for changing color every 7 hit objects
    c = 0
    for i in range(len(res)):
        if (res[i][0] == 1):
            if (c % 7 == 0):
                mis.append([int(x_coor[c]), int(y_coor[c]), int(float(res[i][1]))] + [5,0,"0:0:0:0:"])
            else:
                mis.append([int(x_coor[c]), int(y_coor[c]), int(float(res[i][1]))] + [1,0,"0:0:0:0:"])
            c = c+1
    return mis

# read the all information except timepoints and hitobjects from original osu file and create new contents of osu file stored in list contents 
def read(filepath, mis, bpm, res, x_coor, y_coor):
    contents = []
    tp = [[int(1000 * x[3]), 60000 / x[2]] for x  in bpm]

    with open(filepath, 'r') as my_file:
        csvreader = csv.reader(my_file)
        target = "Creator"
        #change the creator and version of original osu file
        for line in csvreader:
            if len(line) == 0:
                contents.append(line)
            else:
                l = line[0].split(':')
                if target not in l[0]:
                    contents.append(line)
                else:
                    contents.append(['Creator:Luying and Mengwei'])
                    break

        target = "Version"
        for line in csvreader:
            if len(line) == 0:
                contents.append(line)
            else:
                l = line[0].split(':')
                if target not in l[0]:
                    contents.append(line)
                else:
                    contents.append(['Version:Luying and Mengwei'])
                    break

        # delete the BeatmapID if needed
        target = "BeatmapID"
        for line in csvreader:
            if len(line) != 0:
                l = line[0].split(':')
                if target not in l[0]:
                    contents.append(line)
                else:
                    break
            else:
                contents.append(line)

        #add new Timepoints
        target = "[TimingPoints]"
        for line in csvreader:
            if target not in line:
                contents.append(line)
            else:
                contents.append(line)
                break

        next_row = next(csvreader) 
        timing_poing_extra = next_row[2:]
        for x in tp:
            contents.append(x + timing_poing_extra)
        for line in csvreader:
            if len(line) == 0:
                contents.append(line)
                break
        
        # add new hit objects
        target = "[HitObjects]"
        for line in csvreader:
            if target not in line:
                contents.append(line)
            else:
                contents.append(line)
                break
        hits = merge(mis, res, x_coor, y_coor)
        contents += hits

        return (contents)

# the result of this function is used for generating new coordinate
def getinterval(is_hit):
    interval = []
    prev = 0
    for i in range(len(is_hit)):
        if (is_hit[i] == 1):
            interval.append(int(i - prev))
            prev = i
    return interval


#normalized the properties that is it hit object of testing result
def target_norm(col):
    min_bound = min(col)
    max_bound = max(col)
    for i in range(len(col)):
        col[i] = (col[i] - min_bound) / (max_bound - min_bound)
    return col

# change the properties that is it hit object to either 1 or 0 of testing result using threshold
def threshold(col, thresh):
    for i in range(len(col)):
        if col[i] >= thresh:
            col[i] = 1
        else:
            col[i] = 0
    return col


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise argparse.ArgumentTypeError('the number of argument has to be 2')
        exit(-1)

    path = "/Users/yanmingjun/Documents/osu-audio-feature-extract/Data/Beatmaps02/13019 Daisuke Achiwa - BASARA/Trainings/"
    output_path = "/Users/yanmingjun/Documents/osu-audio-feature-extract/Data/Trainables/"
    osu_path = "/Users/yanmingjun/Documents/osu-audio-feature-extract/Data/Beatmaps02/13019 Daisuke Achiwa - BASARA/"
    output_file = os.path.join(output_path, "basara_result.csv")
    mis_file = os.path.join(path, "mis.v1.csv")
    dy_bpm_file = os.path.join(path, "timing_points.v1.csv")
    osu_file = os.path.join(osu_path, "Daisuke Achiwa - BASARA (100pa-) [BASARA].osu")
    
    # read mis
    mis = np.loadtxt(mis_file, delimiter = ',')
    mis = mis[:,1:2]

    # read dynamic bpm
    bpm = np.loadtxt(dy_bpm_file, delimiter = ',')

    # read is it hit property
    res = np.loadtxt(output_file, delimiter = ',')
    is_hit = res[:,2]
    is_hit = target_norm(is_hit)
    is_hit = threshold(is_hit, 0.55)
    res = np.vstack([is_hit]).transpose() 

    #create new coordinate
    interval = getinterval(is_hit)    
    coor = np.array(generate_map_coordinate(interval))
    x_coor = coor[:, 0]
    y_coor = coor[:, 1]

    # call to create new osu file
    text = read(osu_file, mis, bpm, res, x_coor, y_coor)

    # write in osu file
    with open(sys.argv[1], "w") as file:
        writer = csv.writer(file)
        writer.writerows(text)