import sys
import argparse
from osu_getInfo import search
import csv

# extract hit objects from osu file
def getHitobject(file):
    hitobject = []
    with open(file, 'r') as my_file:
        csvreader = csv.reader(my_file)
        target = "[HitObjects]"
        # find the string "[HitObjects]" in file
        for line in csvreader:
            if target in line:
                break
        
        # the next line until the empty line is the hit object
        for tmp in csvreader:
            # check is it an empty line
            if len(tmp) != 0:
                # extract the first 5 elements of each hit object
                # and check is each hit object contains 0:0:0:0: at the last element, added if not avaliable
                if len(tmp) == 5:
                    tmp = list(map(int, tmp))
                    for i in range(4):
                        tmp.append(0)
                else:
                    lastele = tmp[len(tmp)-1]
                    tmp = tmp[0:5]
                    tmp = list(map(int, tmp))
                    addition = lastele.split(":")
                    if len(addition) == 4:
                        for i in range(4):
                            tmp.append(int(addition[i]))
                    else:
                        for i in range(4):
                            tmp.append(0)
                hitobject.append(tmp)
            else: 
                break	
    return hitobject	

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise argparse.ArgumentTypeError('the number of argument has to be 2')
        exit(-1)

    hitobject = getHitobject(sys.argv[1])

    # output the hit objects for saving
    writer = csv.writer(sys.stdout)
    writer.writerows(hitobject)
