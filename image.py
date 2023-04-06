from PIL import Image as PILImage
import pdb
from math import floor, ceil
import statistics
from kernel import Kernel

# ### Part 1
# - [x] Crop an image
# - [x] Flip image horizontally
# - [x] Flip image vertically
# - [] Scale image
#     - [x] Nearest Neighbour
#     - [x] Bilinear
#     - [] Bicubic
# - [] Rotate image (Nearest Neighbour)

# ### Part 2
# - [X] Linear grey level mappings
# - [?] Power law grey level mappings
# - [X] Histogram calculation
# - [X] Histogram equalization

# ### Part 3+4
# - [X] Calculate convolution of a rectangular kernel with zero padding
# - [X] Linear filtering
# - [X] Non-linear filtering
#   - [x] Min 
#   - [x] max 
#   - [X] median filtering

# ### Bonus
# - [X] Negatives
# - [X] Circular Padding
# - [X] Reflected padding

def zero_padding(x,y,img):

    if (x < 0 or x >= img.width or y < 0 or y >= img.height):
        return (0,0,0)
    else:
        return img.pixels[x,y]

def circular_padding(x,y,img):
    return img.pixels[x%img.width, y%img.height]

def reflected_padding(x,y,img):

    x_mod = (x//img.width)%2
    y_mod = (y//img.height)%2

    if x_mod == 0:
        x = x % img.width
    else:
        x = img.width - (x % img.width) - 1

    if y_mod == 0:
        y = y % img.height
    else:
        y = img.height - (y % img.height) - 1 

    return img.pixels[x,y]

class Image:

    def __init__(self, fileName=None, padding=zero_padding, height = None, width = None):

        # self.fileName = fileName

        if fileName != None:
            self.image = PILImage.open(fileName)
            self.pixels = self.image.load()
            self.width, self.height = self.image.size

        elif height != None and width != None:
            self.image = PILImage.new('RGB', (width,height))
            self.pixels = self.image.load()
            self.width = width
            self.height = height
        
        self.padding = padding

    def get_pixel(self, x, y):
        return self.padding(x, y, self)

    def set_pixel(self,x,y,pixel_intensity):
        self.pixels[x,y] = pixel_intensity

    def set_pixel_color(self,x,y,pixel_intensity,i):
        temp = list(self.pixels[x,y])
        temp[i] = pixel_intensity
        self.pixels[x,y] = tuple(temp)

    def copy_blank(self):
        new_image = Image(height = self.height, width = self.width)
        return new_image

    def copy_info(self,new):

        self.image = new.image
        self.height = new.height
        self.width = new.width
        self.pixels = new.pixels
        self.padding = new.padding

    def flip_horizontally(self):

        new_image = self.copy_blank()

        for i in range(self.width):
            for j in range(self.height):

                new_image.set_pixel(self.width - i - 1, j, self.get_pixel(i,j))

        self.copy_info(new_image)

    def flip_veritcally(self):

        new_image = self.copy_blank()

        for i in range(self.width):
            for j in range(self.height):

                new_image.set_pixel(i, self.height - j - 1, self.get_pixel(i,j))

        self.copy_info(new_image)
    
    def crop(self,x1,y1,x2,y2):

        new_image = Image(height = y2-y1, width = x2-x1)


        for i in range(x2-x1):
            for j in range(y2-y1):
                new_image.set_pixel(i,j,self.get_pixel(x1 + i, y1 + j))

        self.copy_info(new_image)

    def scale_nearest_neighbour(self,x_factor,y_factor):

        new_height = floor(y_factor * self.height)
        new_width = floor(x_factor * self.width)

        new_image = Image(height = new_height, width = new_width)

        for i in range(new_image.width):
            for j in range(new_image.height):

                x = i/x_factor
                y = j/y_factor

                round(x)
                round(y)

                if(y >= self.height):
                    y = self.height - 1
                
                if(x >= self.width):
                    x = self.width - 1

                new_image.set_pixel(i,j,self.get_pixel(x,y))

        self.copy_info(new_image)

    def scale_bilinear(self,x_factor,y_factor):

        new_height = floor(y_factor * self.height)
        new_width = floor(x_factor * self.width)

        new_image = Image(height = new_height, width = new_width)

        for i in range(new_image.width):
            for j in range(new_image.height):

                x = i / x_factor
                y = j / y_factor

                x2 = ceil(x)
                x1 = floor(x)
                y2 = ceil(y)
                y1 = floor(y)

                wx = (x-x1)
                wy = (y - y1)

                for k in range(len(self.image.mode)):
                    
                    X = self.get_pixel(x1,y1)[k] * ( 1 - wx) +  self.get_pixel(x2,y1)[k] * wx
                    Y = self.get_pixel(x1,y2)[k] * ( 1 - wx) +  self.get_pixel(x2,y2)[k] * wx

                    Z = X*(1 - wy) + Y*(wy)

                    

                    Z = round(Z)

                    new_image.set_pixel_color(i,j,Z,k)

        self.copy_info(new_image)
    
    def filter_max(self,x,y):

        temp_image = self.copy_blank()

        for i in range(self.width):
            for j in range(self.height):

                max = 0
                for element in self.get_pixel(i,j):
                    max+=element
                
                max_tuple = self.get_pixel(i,j)

                for k in range(floor(-x/2), ceil(x/2)):
                    for l in range(floor(-y/2),ceil(y/2)):

                        temp = 0
                        temp_tuple = self.get_pixel(i+k,j+l)

                        for element in temp_tuple:
                            temp+=element

                        if temp > max:
                            max = temp
                            max_tuple = temp_tuple
                
                temp_image.set_pixel(i,j,max_tuple)

        self.copy_info(temp_image)
        
    def filter_min(self,x,y):

        temp_image = self.copy_blank()

        for i in range(self.width):
            for j in range(self.height):

                min = 0
                for element in self.get_pixel(i,j):
                    min+=element
                
                min_tuple = self.get_pixel(i,j)

                for k in range(floor(-x/2), ceil(x/2)):
                    for l in range(floor(-y/2),ceil(y/2)):

                        temp = 0
                        temp_tuple = self.get_pixel(i+k,j+l)

                        for element in temp_tuple:
                            temp+=element

                        if temp < min:
                            min = temp
                            min_tuple = temp_tuple
                
                temp_image.set_pixel(i,j,min_tuple)

        self.copy_info(temp_image)

    def filter_median(self,x,y):

        temp_image = self.copy_blank()

        for i in range(self.width):
            for j in range(self.height):

                tuple_list = []
                
                for k in range(floor(-x/2), ceil(x/2)):
                    for l in range(floor(-y/2),ceil(y/2)):

                        tuple_list.append(self.get_pixel(i+k,j+l))
                
                new_pixel = ()

                for k in range(len(self.image.mode)):

                    median_list = []

                    for element in tuple_list:
                        median_list.append(element[k])

                    temp_tup = (floor(statistics.median(median_list)),)

                    new_pixel = new_pixel + temp_tup


                temp_image.set_pixel(i,j,new_pixel)
                

        self.copy_info(temp_image)
                        
    def power_mapping(self,c,p):

        temp_image = self.copy_blank()
     
        for i in range(self.width):
            for j in range(self.height):

                new_pixel = ()

                for element in self.get_pixel(i,j):

                    temp_tuple = (floor(pow(element, p) * c),)
                    new_pixel = new_pixel + temp_tuple
                
                temp_image.set_pixel(i,j,new_pixel)   

        self.copy_info(temp_image)

    def linear_mapping(self,a,b):

        temp_image = self.copy_blank()
     
        for i in range(self.width):
            for j in range(self.height):

                new_pixel = ()

                for element in self.get_pixel(i,j):

                    temp_tuple = (floor(element * a + b),)
                    new_pixel = new_pixel + temp_tuple
                
                temp_image.set_pixel(i,j,new_pixel)   

        self.copy_info(temp_image)

    def negative(self):

        temp_image = self.copy_blank()

        for i in range(self.width):
            for j in range(self.height):

                new_pixel = ()

                for element in self.get_pixel(i,j):

                    temp_tuple = (255-element,)
                    new_pixel = new_pixel + temp_tuple
                
                temp_image.set_pixel(i,j,new_pixel)

        self.copy_info(temp_image)


    def get_histogram(self):

        histograms = []

        for char in self.image.mode:

            temp_histogram = {}
            histograms.append(temp_histogram)

            
        for k in range(len(histograms)):

            for i in range(self.width):
                for j in range(self.height):
                        
                    intensity = self.get_pixel(i,j)[k]

                    if intensity in histograms[k]:
                        histograms[k][intensity]+= 1 

                    else:
                        histograms[k][intensity] = 1

        return histograms

    def equalize_histogram(self):

        histograms = self.get_histogram()
        pixel_count = self.height * self.width
        
        new_values = []

        for i in range(len(histograms)):

            pdf = []

            for j in range(256):

                if j in histograms[i]:
                    pdf.append(histograms[i][j]/pixel_count)

                else:
                    pdf.append(0)


            cdf = []
            for j in range(len(pdf)):
                
                temp = 0

                if(j != 0):
                    temp+= cdf[j-1]

                temp+=pdf[j]

                cdf.append(temp)

            sk = []

            for j in range(len(cdf)):
                sk.append(ceil(cdf[j] * 255))

            new_values.append(sk)

        for i in range(self.width):
            for j in range(self.height):

                old_pixel = self.get_pixel(i,j)
                new_pixel = ()

                for k in range(len(old_pixel)):
                    new_pixel+=(new_values[k][old_pixel[k]],)

                self.set_pixel(i,j,new_pixel)





temp = Image(fileName = "./sam.jpg",padding = reflected_padding)


#temp.scale_nearest_neighbour(0.19,0.19)
#temp.scale_bilinear(0.19,0.19)
#temp.negative()
#temp.power_mapping(1,0.5)
#temp.filter_median(5,5)
temp.negative()

temp.equalize_histogram()


array = [[-1,-1,-1],[0,0,0],[1,1,1]]

kernel = Kernel(array)

#kernel.convulve(temp)


temp.image.show()

temp.image.save("temp.jpg")