#!/usr/bin/python
import sys
import math
import csv
from ast import literal_eval


reader = csv.reader(sys.stdin, delimiter=';')

for line in reader:
    index = literal_eval(line[0])
    # This will eval the pixel as a tuple
    pixel = literal_eval(line[1])

    luminance = (0.2126 * pixel[0]) + (0.7152 * pixel[1]) + (0.0722 * pixel[2])
    # Output index and luminance
    print "{0}\t{1}\t{2}".format(index[0], index[1], int(math.floor(luminance)))
