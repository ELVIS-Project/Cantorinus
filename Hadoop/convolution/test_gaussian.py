from ast import literal_eval
import convolution
from PIL import Image
import csv
import sys

width, height = 512, 512

x, y = 128, 256


output_image = Image.new("RGB", (width, height), "white")
pixels = output_image.load()

gaussian_matrix = convolution.generate_gaussian_convolution_matrix(3, x, y, width, height)

for i in range(width):
    for j in range(height):
        value = int(gaussian_matrix[i][j] * 255)
        pixels[i,j] = (value, value, value)

output_image.save("test_gaussian.png")