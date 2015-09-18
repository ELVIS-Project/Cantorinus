import math

def convolution(matrix, pixels, x, y, pixels_width, pixels_height):
    width = len(matrix)
    height = len(matrix[0])

    output = [0, 0, 0]

    for channel in range(3):
        for i in range(width):
            for j in range(height):
                current_x = x - (width / 2) + i
                if current_x < 0:
                    current_x = 0
                elif current_x >= pixels_width:
                    current_x = pixels_width - 1

                current_y = y - (height / 2) + j
                if current_y < 0:
                    current_y = 0
                elif current_y >= pixels_height:
                    current_y = pixels_height - 1

                pixel = pixels[current_x, current_y]
                output[channel] = int(output[channel] + (matrix[i][j] * pixel[channel]))


    return output

def complete_convolution(pixels, convolution, width, height):
    output = [0, 0, 0]
    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]
            multiplier = convolution[x][y]
            for channel in range(3):
                output[channel] = output[channel] + pixel[channel] * multiplier
    return tuple(output)

def quicker_convolution(pixels, convolution, x, y, width, height):
    pass

def generate_centered_gaussian_convolution_matrix(sigma, width, height):
    center_x = width / 2
    center_y = height / 2
    return generate_gaussian_convolution_matrix(sigma, center_x, center_y, width, height)

def generate_gaussian_convolution_matrix(sigma, x, y, width, height):
    total = 0
    output = [[0 for output_y in xrange(height)] for output_x in xrange(width)]
    for i in range(width):
        for j in range(height):
            # print abs(i - x), abs(j - y)
            output[i][j] = round(gaussian(abs(i - x), abs(j - y), sigma), 5)
            # Add to total
            total = total + output[i][j]
    # Finally, divide all values by the total
    for i in range(width):
        for j in range(height):
            output[i][j] = output[i][j] / total
    return output

def gaussian(x, y, sigma):
    return (1 / math.sqrt(2 * math.pi * math.pow(sigma, 2))) * math.pow(math.e, (0 - (math.pow(x, 2) + math.pow(y, 2)) / (2 * math.pow(sigma, 2))))

