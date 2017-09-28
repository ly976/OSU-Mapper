import sys
import argparse
from osuFileParser import searchSublevel

if __name__ == "__main__":
	if len(sys.argv) != 2:
		raise argparse.ArgumentTypeError('the number of argument has to be 2')
		exit(-1)
	searchSublevel("General", "AudioFilename")

