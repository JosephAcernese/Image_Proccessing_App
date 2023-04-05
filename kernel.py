from PIL import Image as PILImage
import pdb
from math import floor, ceil
import statistics

class Kernel:

    def __init__(self,array):
        self.array = array
        self.height = len(array)
        self.width = len(array[0])


    def convulve(self,image):

        temp_image = image.copy_blank()
        mid_height = floor(self.height/2)
        mid_width = floor(self.width/2)

        for i in range(image.width):
            for j in range(image.height):

                new_pixel = ()

                for m in range(len(image.image.mode)):

                    sum = 0

                    for k in range(self.width):
                        for l in range(self.height):

                            sum+= self.array[k][l] * image.get_pixel(i - mid_width + k, j - mid_height + l)[m]


                    sum = floor(sum)
                    new_pixel = new_pixel + (sum,)


                temp_image.set_pixel(i,j,new_pixel)

        image.copy_info(temp_image)