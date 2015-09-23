from PIL import Image
import sys

image_name, output_name = sys.argv[1], sys.argv[2]

image = Image.open(image_name)
pixels = image.load()
size = image.size

output_file = open(output_name, "w")

for x in range(size[0]):
    for y in range(size[1]):
        output_file.write("{0};{1}\n".format((x,y), pixels[x,y]))

output_file.close()