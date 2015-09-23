from PIL import Image

image = Image.open("sample.jpg")
pixels = image.load()
size = image.size

output_file = open("input.csv", "w")

for x in range(size[0]):
    for y in range(size[1]):
        output_file.write("{0};{1}\n".format((x,y), pixels[x,y]))

output_file.close()