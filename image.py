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

# ### Part 2
# - [X] Linear grey level mappings
# - [X] Power law grey level mappings
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
# - [] Rotate image (Nearest Neighbour)


#Zero padding function
def zero_padding(x,y,img):

    #If the index is out of range of the image
    if (x < 0 or x >= img.width or y < 0 or y >= img.height):


        pixel = ()
        
        #Create a 0 pixel with the same length as the mode
        for i in range(len(img.image.mode)):
            pixel = pixel + (0,)

        print(pixel)

        return pixel

    #If its within coordinates
    else:
        return img.pixels[x,y]


#Circular padding function
def circular_padding(x,y,img):

    #Returns the pixel within the range of the image
    return img.pixels[x%img.width, y%img.height]


#Reflected padding function
def reflected_padding(x,y,img):

    #Determine whether the coordinates are an even or odd number of instances away
    x_mod = (x//img.width)%2
    y_mod = (y//img.height)%2

    #If x doesnt need to be inverted
    if x_mod == 0:
        x = x % img.width

    #If x needs to be inverted
    else:
        x = img.width - (x % img.width) - 1

    #If y doesnt need to be inverted
    if y_mod == 0:
        y = y % img.height

    #If y needs to be inverted
    else:
        y = img.height - (y % img.height) - 1 

    #Return pixel
    return img.pixels[x,y]


#Image class, used for all image handling within this program
class Image:

    #Innit function is able to handle: Filename or high/width
    #Filename loads an image in from the files
    #Height/Width creates a blank image with the same length and height, defaults to RBG
    def __init__(self, fileName=None, padding=zero_padding, height = None, width = None):

        #If filename is given
        if fileName != None:
            self.image = PILImage.open(fileName)
            self.pixels = self.image.load()
            self.width, self.height = self.image.size

        #If height/width is given
        elif height != None and width != None:
            self.image = PILImage.new('RGB', (width,height))
            self.pixels = self.image.load()
            self.width = width
            self.height = height
        
        #Set padding
        self.padding = padding

    #Call padding function
    def get_pixel(self, x, y):
        return self.padding(x, y, self)

    #Set pixel value
    def set_pixel(self,x,y,pixel_intensity):
        self.pixels[x,y] = pixel_intensity

    #Unused function which changes one index within the pixel tuple
    def set_pixel_color(self,x,y,pixel_intensity,i):
        temp = list(self.get_pixel(x,y))
        temp[i] = pixel_intensity
        self.pixels[x,y] = tuple(temp)

    #Create a new blank image with the same size as the current
    def copy_blank(self):
        new_image = Image(height = self.height, width = self.width, padding = self.padding)
        return new_image

    #Create a new image with all the same information as the old one
    #Unimplemented in any other parts of code
    def copy_info(self,new):

        self.image = new.image
        self.height = new.height
        self.width = new.width
        self.pixels = new.pixels
        self.padding = new.padding


    #Function which flips current image horizontally
    def flip_horizontally(self):

        #Create a copy of the image
        new_image = self.copy_blank()

        #Loop through every pixel
        for i in range(self.width):
            for j in range(self.height):

                #Invert the image along the x axis
                new_image.set_pixel(self.width - i - 1, j, self.get_pixel(i,j))

        #Copy new image back to the original 
        self.copy_info(new_image)

    #Function which flips image vertically
    def flip_veritcally(self):

        #Create a copy of the image
        new_image = self.copy_blank()

        #Loop through every pixel
        for i in range(self.width):
            for j in range(self.height):

                #Invert the image on the y axis
                new_image.set_pixel(i, self.height - j - 1, self.get_pixel(i,j))

        #Copy image back to original
        self.copy_info(new_image)
    

    #Function which crops an image using two sets of coordinate
    def crop(self,x1,y1,x2,y2):

        #Create a new image with the size of the new image
        new_image = Image(height = y2-y1, width = x2-x1,padding = self.padding)

        #Loop through every pixel in the new image
        for i in range(x2-x1):
            for j in range(y2-y1):
                #Set the current pixel to the relative pixel in the original image
                new_image.set_pixel(i,j,self.get_pixel(x1 + i, y1 + j))

        #Copy image back
        self.copy_info(new_image)

    #Function which scales an image using the nearest neighbour method
    def scale_nearest_neighbour(self,x_factor,y_factor):

        #Calculate the new height and width based on the x and y factors
        new_height = floor(y_factor * self.height)
        new_width = floor(x_factor * self.width)

        #Create new image with the new height and width
        new_image = Image(height = new_height, width = new_width, padding = self.padding)

        #Loop through every pixel in the new image
        for i in range(new_image.width):
            for j in range(new_image.height):

                #Calculate the relative position of the pixel in the new image 
                x = i/x_factor
                y = j/y_factor

                round(x)
                round(y)

                #Edge case where pixel ends up being beyond originals range
                if(y >= self.height):
                    y = self.height - 1
                
                if(x >= self.width):
                    x = self.width - 1

                #Set new pixel value to the relative position's pixel value
                new_image.set_pixel(i,j,self.get_pixel(x,y))

        #Copy the image's information back
        self.copy_info(new_image)




    #Function which scales an image using the bilinear method
    def scale_bilinear(self,x_factor,y_factor):

        #get the height and width of the new image
        new_height = floor(y_factor * self.height)
        new_width = floor(x_factor * self.width)

        #create the new image
        new_image = Image(padding = self.padding, height = new_height, width = new_width)

        #loop through every pixel in the new image
        for i in range(new_image.width):
            for j in range(new_image.height):

                #Calculate the relative position in the original image
                x = i / x_factor
                y = j / y_factor

                #Calculate the four closest points
                x2 = ceil(x)
                x1 = floor(x)
                y2 = ceil(y)
                y1 = floor(y)

                wx = (x-x1)
                wy = (y - y1)

                new_pixel = ()


                #For every dimension in the image
                for k in range(len(self.image.mode)-1):

                    #Calculate the weight between 2 sets of 2 points
                    X = (self.get_pixel(x1,y1))[k] * ( 1 - wx) +  (self.get_pixel(x2,y1))[k] * wx
                    Y = (self.get_pixel(x1,y2))[k] * ( 1 - wx) +  (self.get_pixel(x2,y2))[k] * wx

                    #Calculate the weight between the 4 points
                    Z = X*(1 - wy) + Y*(wy)

                    #Round it off
                    Z = round(Z)

                    new_pixel = new_pixel + (Z,)
                
                new_image.set_pixel(i,j,new_pixel)


        #Copy image
        self.copy_info(new_image)
    

    #Function which takes an image and performs a max filter operation
    def filter_max(self,x,y):

        #Copy image
        temp_image = self.copy_blank()

        #Iterate through every pixel
        for i in range(self.width):
            for j in range(self.height):

                #Get first max
                max = 0
                for element in self.get_pixel(i,j):
                    max+=element
                
                #I forget what this does tbh
                max_tuple = self.get_pixel(i,j)

                #Loop through all pixels within range
                for k in range(floor(-x/2), ceil(x/2)):
                    for l in range(floor(-y/2),ceil(y/2)):

                        #Get current tuple
                        temp = 0
                        temp_tuple = self.get_pixel(i+k,j+l)

                        #Get element
                        for element in temp_tuple:
                            temp+=element

                        #Compare to max
                        if temp > max:
                            max = temp
                            max_tuple = temp_tuple
                
                #Set pixel to new max
                temp_image.set_pixel(i,j,max_tuple)

        #Copy image over
        self.copy_info(temp_image)
        
    #Function which performs a minimum filter operation
    def filter_min(self,x,y):

        #Copy image
        temp_image = self.copy_blank()

        #loop through every pixel
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





# temp = Image(fileName = "./biden.png",padding = reflected_padding)


#temp.scale_nearest_neighbour(3,4)
#temp.scale_bilinear(0.19,0.19)
#temp.negative()
#temp.power_mapping(1,0.5)
#temp.filter_median(5,5)
#temp.negative()

#temp.equalize_histogram()

# temp.crop(150,100,400,400)
# temp.equalize_histogram()
# temp.negative()
# temp.crop(-500,-500,500,500)
# temp.scale_bilinear(0.1,0.1)
# temp.crop(-500,-500,500,500)

#temp.crop(-200,-200,500,500)
user_choice = -1
image = None

print("The Image Processing App")


#Loop for user prompts
while(user_choice != 18):    

    #print options
    print("1. Open an image")
    print("2. Save the image")
    print("3. Display image")
    print("4. Padding type")
    print("5. Crop")
    print("6. Flip horizontally")
    print("7. Flip vertically")
    print("8. Scale Nearest Neighbour")
    print("9. Scale bilinear")
    print("10. Negative")
    print("11. Min Filter")
    print("12. Max Filter")
    print("13. Median filter")
    print("14. Linear Mapping")
    print("15. Power Mapping")
    print("16. Hstogram equalization")
    print("17. Kernel Convolution")
    print("18. Quit")


    #Prompt user
    user_input = input("Enter an option: ")

    #convert input to an integer
    try:
        user_choice = int(user_input)
    except:
        print("ERROR: Invalid input, try again")
        input()
        continue

    #If they're openeing a file
    if(user_choice == 1):

        fileName = input("Enter filename: ")
        
        #Try to open
        try:
            image = Image(fileName = fileName)
            print("Image loaded")

        #If it fails
        except:
            print("ERROR: Unable to open file")
            input()
            continue

    #If an image hasnt been uploaded yet 
    if(image == None and (user_choice != 12 or user_choice != 1)):
        print("ERROR: Cannot perform operartion with no image")
        input()
        continue

    #IF save option is picked
    if(user_choice == 2):

        fileName = input("Enter filename: ")

        #Attempt to save
        try: 
            image.image.save(fileName)
            print("Image saved")

        #If it couldnt be saved
        except:
            print("ERROR: Unable to save image")

    #display image
    if(user_choice == 3):
        image.image.show()
        print("Image displayed")


    #If user is changing padding types
    if(user_choice == 4):

        #Prompt user
        print("1. Zero Padding")
        print("2. Circular Padding")
        print("3. Reflect Padding")
        user_input = input("Choose an option: ")

        try: 
            padding_choice = int(user_input)

        except:
            print("ERROR: Invalid input")
            continue

        #Set padding to current type
        if(padding_choice == 1):
            image.padding = zero_padding
        
        elif(padding_choice == 2):
            image.padding = circular_padding

        elif(padding_choice == 3):
            image.padding = reflected_padding

        #If invalid numbers entered
        else:
            print("ERROR: Invalid number")
            input()
            continue

        #Print confirmation
        print("Padding type set")

    #If user is cropping
    if(user_choice == 5):

        #Get first set of coordinates
        print("First position")
        str_x1 = input("Enter x coordinate: ")
        str_y1 = input("Enter y coordinate: ")
        print()

        #Get second set of coordinates
        print("Second position")
        str_x2 = input("Enter x coordinate: ")
        str_y2 = input("Enter y coordinate: ")

        try:
            #Convert each input to integer
            x1 = int(str_x1)
            x2 = int(str_x2)
            y1 = int(str_y1)
            y2 = int(str_y2)

            #Crop the image
            image.crop(x1,y1,x2,y2)
            print("Image cropped successfully")

        #If the conversions fail
        except: 
            print("ERROR: Invalid input")
            input()
            continue

    #If user is flipping
    if(user_choice==6):
        image.flip_horizontally()
        print("Image flipped")

    #If user is flipping
    if(user_choice == 7):
        image.flip_veritcally()
        print("Image flipped")

    #If user is scaling
    if(user_choice == 8):

        x_str = input("Enter x factor: ")
        y_str = input("Enter y factor: ")
    
        try:
            x = float(x_str)
            y = float(y_str)

            image.scale_nearest_neighbour(x,y)
            print("Image scaled")

        except:
            print("ERROR: Invalid input")
            input()
            continue

    #If user is scaling
    if(user_choice == 9):

        #Prompt user
        x_str = input("Enter x factor: ")
        y_str = input("Enter y factor: ")
    
        #Try to scale image
        try:
            x = float(x_str)
            y = float(y_str)

            image.scale_bilinear(x,y)
            print("Image scaled")

        #If errors encountered
        except:
            print("ERROR: Invalid input")
            input()
            continue

    #If user is taking negative
    if(user_choice == 10):
        image.negative()
        print("Negative filter applied")

    #If min filter is being applied 
    if(user_choice == 11):

        #Get distance
        dist_str = input("Enter distance: ")

        #Try to apply filter
        try:
            dist = int(dist_str)
            filter_min(dist*2 + 1, dist*2 + 1)
            print("Min filter applied")

        #If input was invalid
        except:
            print("ERROR: Invalid input")
            input()
            continue


    #If max filter is being applied 
    if(user_choice == 12):

        #Get distance
        dist_str = input("Enter distance: ")

        #Try to apply filter
        try:
            dist = int(dist_str)
            filter_max(dist*2 + 1, dist*2 + 1)
            print("Max filter applied")

        #If input was invalid
        except:
            print("ERROR: Invalid input")
            input()
            continue

    #If median filter is being applied 
    if(user_choice == 13):

        #Get distance
        dist_str = input("Enter distance: ")

        #Try to apply filter
        try:
            dist = int(dist_str)
            filter_median(dist*2 + 1, dist*2 + 1)
            print("Median filter applied")

        #If input was invalid
        except:
            print("ERROR: Invalid input")
            input()
            continue

    #If they want linear mapping
    if(user_choice == 14):

        #Prompt user
        coeff_str = input("Enter coefficient: ")
        const_str = input("Enter constant: ")

        #Try to apply filter
        try: 
            coeff = float(coeff_str)
            const = float(const_str)

            image.linear_mapping(coeff, const)
            print("Linear mapping applied")

        except:
            print("ERROR: Invalid input")
            input()
            continue


    #If they want Power mapping
    if(user_choice == 15):

        #Prompt user
        exp_str = input("Enter exponent: ")
        const_str = input("Enter coefficient: ")

        #Try to apply filter
        try: 
            exponent = float(exp_str)
            const = float(const_str)

            image.power_mapping(exponent, const)
            print("Power mapping applied")

        except:
            print("ERROR: Invalid input")
            input()
            continue

    #If user wants to equalize histogram
    if(user_choice == 16):
        image.equalize_histogram()
        print("Equalization applied")

    #If user wants to apply convolution
    if(user_choice == 17):

        print()


    #If user devices to quit
    if(user_choice == 18):
        break

    input()








# array = [[-1,-1,-1],[0,0,0],[1,1,1]]
# kernel = Kernel(array)
# #temp.filter_min(5,5)

#kernel.convulve(temp)


# temp.image.show()

# temp.image.save("temp.jpg")