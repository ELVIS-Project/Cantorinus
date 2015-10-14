#!/usr/bin/env ../app_env/bin/python

from ast import literal_eval
from PIL import Image
import csv
import sys
import convolution

image = Image.open("mandrill.png")
pixels = image.load()
size = image.size

reader = csv.reader(sys.stdin, delimiter=';')
gaussian_blur = convolution.generate_centered_gaussian_convolution_matrix(5, 16, 16)

for line in reader:
    index = literal_eval(line[0])
    x = index[0]
    y = index[1]

    new_pixel = convolution.convolution(convolution.unsharp_kernel, pixels, x, y, size[0], size[1])

    print("{0}\t{1}\t{2}\t{3}\t{4}".format(x, y, int(new_pixel[0]), int(new_pixel[1]), int(new_pixel[2])))

