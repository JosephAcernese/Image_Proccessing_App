from PIL import Image as PILImage
import pdb
from math import floor, ceil
import statistics
from kernel import Kernel
from image import Image
from image import zero_padding
from image import reflected_padding
from image import circular_padding

#Intialize variables
user_choice = -1
image = None



#Loop for user prompts
while(user_choice != 18):    


    print("The Image Processing App")

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
    if(image == None and (user_choice != 18 or user_choice != 1)):
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
            image.filter_min(dist*2 + 1, dist*2 + 1)
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
            image.filter_max(dist*2 + 1, dist*2 + 1)
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
            image.filter_median(dist*2 + 1, dist*2 + 1)
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

        #Get dimensions
        size_str = input("Enter kernel size: ")

        #Convert to int
        try:
            size = int(size_str)

        except:
            print("ERROR: Invalid input")

        #Intial kernel array
        k_array = []

        #Get the number of rows from the user
        for i in range(size):
            row_str = input("Enter row: ")
            array = list(map(float, row_str.split()))
            k_array.append(array)

        kernel = Kernel(k_array)

        kernel.convulve(image)

        print("Convolution applied")



    #If user devices to quit
    if(user_choice == 18):
        break

    input()


