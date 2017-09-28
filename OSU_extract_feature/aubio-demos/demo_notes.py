#! /usr/bin/env python

import sys
from aubio import source, notes

if len(sys.argv) < 2:
    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

downsample = 1
samplerate = 44100 // downsample
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

win_s = 1024 // downsample # fft size
hop_s = 512 // downsample # hop size

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate

tolerance = 0.8

notes_o = notes("default", win_s, hop_s, samplerate)

# cordinate
cordinate_samples = [
    (352, 332), (224, 232)
]
cordinate_samples_max = len(cordinate_samples) - 1
cordinate_i = 0
def cordinate_increase():
    global cordinate_i
    if cordinate_i == cordinate_samples_max:
        cordinate_i = 0
    else:
        cordinate_i += 1
    
def cordinate_current():
    global cordinate_i
    return cordinate_samples[cordinate_i]

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    new_note = notes_o(samples)
    if (new_note[0] != 0):
        time  = total_frames/float(samplerate) * 1000
        cordinate = cordinate_current()
        #note_str = ' '.join(["%.2f" % i for i in new_note])
        print("{x},{y},{time},{type},{hitSound},{addition}".format(
            x=cordinate[0],
            y=cordinate[1],
            time=int(time),
            type=1,
            hitSound=0,
            addition="0:0:0:0:"
        ))
        cordinate_increase()
    total_frames += read
    if read < hop_s: break
