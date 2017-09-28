#! /usr/bin/env python

import sys
from aubio import source, tempo
from numpy import median, diff

sys.setrecursionlimit(50000)

def get_file_bpm(path, params = None):
    if params is None:
        params = {}
    try:
        win_s = params['win_s']
        samplerate = params['samplerate']
        hop_s = params['hop_s']
    except KeyError:
        # default:
        samplerate, win_s, hop_s = 44100, 1024, 512

    print(samplerate, win_s, hop_s)
    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0
    while True:
        print(total_frames, 1)
        samples, read = s()
        print(total_frames, 2)
        try:
            is_beat = o(samples)
            print(total_frames, 3)
            if is_beat:
                this_beat = o.get_last_s()
                beats.append(this_beat)
                #if o.get_confidence() > .2 and len(beats) > 2.:
                #    break
        except:
            print(total_frames, "Error")
        print(total_frames, 4)
        total_frames += read
        #print(beats)
        if read < hop_s:
            break
    print("done loop")
    # Convert to periods and to bpm 
    if len(beats) > 1:
        if len(beats) < 4:
            print("few beats found in {:s}".format(path))
        bpms = 60./diff(beats)
        b = median(bpms)
    else:
        b = 0
        print("not enough beats found in {:s}".format(path))
    return b


if __name__ == '__main__':
    filename = sys.argv[1]
    bpm = get_file_bpm(filename)
    #bpm = get_file_bpm(filename, params = {"samplerate":44100, "win_s":512, "hop_s":256})
    print("{:6s} {:s}".format("{:2f}".format(bpm), filename))
