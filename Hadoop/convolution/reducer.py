#!/usr/bin/env ../app_env/bin/python

import sys
import csv
from PIL import Image

reader = csv.reader(sys.stdin, delimiter='\t')

size = (480, 480)

output_image = Image.new("RGB", size, "white")
pixels = output_image.load()

for line in reader:
    x = int(line[0])
    y = int(line[1])
    r = int(line[2])
    g = int(line[3])
    b = int(line[4])
    # Set the pixel to the luminance
    pixels[x,y] = (r, g, b)

output_image.save("output.png")