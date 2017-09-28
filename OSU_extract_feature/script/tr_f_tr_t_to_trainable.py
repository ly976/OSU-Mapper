import csv 
import sys
import argparse

# merge the training feature and training target into a single matrix used for training
def merge(tr_f, tr_t):
    return [tr_f[i] + tr_t[i] for i in range(len(tr_t))]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise argparse.ArgumentTypeError('the number of argument has to be 3')
        exit(-1)
    
    # read training feature
    with open(sys.argv[1], 'r') as my_file:
        csvreader = csv.reader(my_file)
        tr_f = list(csvreader)
    
    # read training target
    with open(sys.argv[2], 'r') as my_file:
        csvreader = csv.reader(my_file)
        tr_t = list(csvreader)
    
    Train_result = merge(tr_f, tr_t)

    # output training result for saving
    writer = csv.writer(sys.stdout)
    writer.writerows(Train_result)

