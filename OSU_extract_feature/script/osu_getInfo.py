import sys
import argparse
import csv

def search(input, filepath):
	res = []
	with open(filepath, 'r') as my_file:
		csvreader = csv.reader(my_file)
		find = False
		target = "[" + input + "]"
		for line in csvreader:
			if target in line:
				find = True
				break
		if (find):
			for line in csvreader:
				if len(line) != 0:
					res.append(line)
				else: 
					break
			return res
		else:
			print("No such infomation in file")

def searchSublevel(x, y):
	with open(sys.argv[1], 'r') as my_file:
		lines = my_file.readlines()
		line_iter = iter(lines)
		find = False
		target = "[" + x + "]"
		for line in line_iter:
			if target in line:
				find = True
				break
		if (find):
			for line in line_iter:
				if len(line.strip()) != 0:
					if y in line:
						l, r = line.split(':')
						print(r.strip())
						break
				else: 
					print("No such infomation in " + x)
					break			
		else:
			print( "No such infomation in file")


if __name__ == "__main__":
	if len(sys.argv) != 2:
		# print( "usage: inputfile outputfile")
		raise argparse.ArgumentTypeError('the number of argument has to be 2')
		exit(-1)
    # filepath = sys.argv[1]
	# searchSublevel("General", "AudioFilename")

