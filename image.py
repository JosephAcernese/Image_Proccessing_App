from PIL import Image as PILImage
import pdb

# ### Part 1
# - [x] Crop an image
# - [x] Flip image horizontally
# - [x] Flip image vertically
# - [] Scale image
#     - [] Nearest Neighbour
#     - [] Bilinear
#     - [] Bicubic
# - [] Rotate image (Nearest Neighbour)

# ### Part 2
# - [] Linear grey level mappings
# - [] Power law grey level mappings
# - [] Histogram calculation
# - [] Histogram equalization

# ### Part 3+4
# - [ ] Calculate convolution of a rectangular kernel with zero padding
# - [ ] Linear filtering
# - [ ] Non-linear filtering
# - [ ] Min, max, median filtering

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

        else:
            console.log("Shouldnt be here")
        
        self.padding = padding



    def get_pixel(self, x, y):
        return self.padding(x, y, self)

    def set_pixel(self,x,y,pixel_intensity):
        self.pixels[x,y] = pixel_intensity

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


    
    



temp = Image(fileName = "./car.jpeg",padding = zero_padding)


temp.crop(-100,-100,300,300)


temp.image.show()

temp.image.save("temp.jpg")