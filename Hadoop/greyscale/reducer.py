#!/usr/bin/python
import sys
import csv
from PIL import Image

reader = csv.reader(sys.stdin, delimiter='\t')

size = (538, 439)

output_image = Image.new("RGB", size, "white")
pixels = output_image.load()

for line in reader:
    x = int(line[0])
    y = int(line[1])
    luminance = int(line[2])
    # Set the pixel to the luminance
    pixels[x,y] = (luminance, luminance, luminance)

output_image.save("output.png")