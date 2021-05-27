#Step 1: Grayscale image
#Step 2: Gaussian Blur
#Step 3: Canny edge detection
#Step 4: Region of Interest
#Step 5: Bitwise_and
#Step 6: Hough Transform
#Step 7: Optimization
#Step 8: Video

import cv2
import numpy as np
import matplotlib.pyplot as plt

def make_coordinates(image, line_parameters):    #to put the coords for  the line region_of_interest
    try:
        slope ,intercept = line_parameters
    except:
        slope, intercept = 0.001, 0
    y1 = image.shape[0]         #heightof the img    #so both of the lines will have the same verticle coords
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)        #rearragnge y=mx+c so x=....form
    x2 = int((y2 - intercept)/slope)
    return np.array([x1,y1,x2,y2])

def average_slope_intercept(image, lines):
    left_fit = []           #left_fit will contain coords of the line which will display on the left and same for right_fit
    right_fit = []          #2 empty lists are declared
    for line in lines:        #loop through every line
        x1, y1, x2, y2 = line.reshape(4) #reshape each line into a 1d array with 4 elements n unpack the elements of the array into 4 variables.
        parameters = np.polyfit((x1,x2), (y1,y2), 1)  #polyfill will fit a 1st degree polynomianl which will be a linear func of y=mx+c,it's going to fix the ploynomial to x n y points n return a vector of coefficients which describe the slope in the intercept.
                                                    # 3rd arg will fit a polynomial of degree 1 to our x n y points .that way we get the parameters of a linear func.
        slope = parameters[0]         #slope is the 1st element in the array. n intercept is the 2nd elemetn .
        intercept = parameters[1]
        if slope < 0:                 #to check if the slope of the line corresponds to a line of the left side of on the right side.
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) #CONVERT IMG TO  grayscale
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  #using gausian blur to reduce noise in the grayscale image
    canny = cv2.Canny(blur, 50,150)  #applying canny on blur image with low and hight threshold as 50 & 150 //to outline the strongest gradient in thr IMG
    return canny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1,y1,x2,y2 in lines:
            #x1,y1,x2,y2 = line.reshape(4)      #converting 2d line to 1d with 4 coords
            cv2.line(line_image, (x1, y1), (x2, y2), (255,0,0), 10) #(line_image,(1st point of the line segment),(2nd pnt of the line segments),color of the lines i.e blue ,thickness of line i.e 10)
    return line_image
def region_of_interest(image):
    height = image.shape[0] #count the row from 0 as rows are the same as height pretty much
    polygons = np.array([
    [(200, height), (1100, height), (550,250)]
    ]) #(x,y) coordinates to draw the triangle
    mask = np.zeros_like(image) #converting numpy arrays of image to black i.e 0
    cv2.fillPoly(mask, polygons, 255)   #put triangle coordinates on mask img in white colot i.e 255
    masked_image = cv2.bitwise_and(image, mask)          # & operation between mask mg n ROI image which will give only 111 part of triangle in the masked_image
    return masked_image

#the code is for 1 frame of video i.e test_image.jpg
#image = cv2.imread('test_image.jpg')  #read the image and cv2 will return it as an numpy array
#lane_image = np.copy(image)
#canny_image = canny(lane_image)
#cropped_image = region_of_interest(canny_image)       #performing roi on canny img
#lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([()]), minLineLength=40, maxLineGap=5 ) #to detect straight lines
 # args: cropped_image,
 #2nd 3rd args specify the resolution of hough acumulator array i.e;, grid which is 2d of row n cols .So a precision of 2px with 1 deg precision in radians,
 #4th is the threshold value that is minimum no. to get accepted ie., 100
# 5this a placeholder array that we need to pass
# 6th is length of the line in pixel that we'll accept into the output,So less than 40 is not acceptable
# 7th indicates the max distance in pixels betwn lines whcih will be allowed to be connected into the single line instead of being broken up.
#averaged_lines = average_slope_intercept(lane_image, lines)     #passing colored img n sraight lines img
#line_image = display_lines(lane_image, averaged_lines)
#combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)   # add both imgs mul 1st img with 0.8 n 2nd with 1 so 2nd is more weighted than 1st which will show more clear blue lines on the original img,1 is added to the summed img.

#cv2.imshow("result", combo_image)  # 1st arg is the name of window and the 2nd the image that we want to show itself
#plt.imshow(canny) #equivalent of cv2.omshow(canny)
#cv2.waitKey(0)   #this displays the image for a certain amount of milliseconds,so we r setting it to 0 then it'll displays the result window infinitely untill a we press any keyboard keyboard
#plt.show() #equivalent of cv2 show

cap = cv2.VideoCapture("test2.mp4")
while(cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)       #performing roi on canny img
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([()]), minLineLength=40, maxLineGap=5 ) #to detect straight lines
     # args: cropped_image,
     #2nd 3rd args specify the resolution of hough acumulator array i.e;, grid which is 2d of row n cols .So a precision of 2px with 1 deg precision in radians,
     #4th is the threshold value that is minimum no. to get accepted ie., 100
    # 5this a placeholder array that we need to pass
    # 6th is length of the line in pixel that we'll accept into the output,So less than 40 is not acceptable
    # 7th indicates the max distance in pixels betwn lines whcih will be allowed to be connected into the single line instead of being broken up.
    averaged_lines = average_slope_intercept(frame, lines)     #passing colored img n sraight lines img
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)   # add both imgs mul 1st img with 0.8 n 2nd with 1 so 2nd is more weighted than 1st which will show more clear blue lines on the original img,1 is added to the summed img.

    cv2.imshow("result", combo_image)  # 1st arg is the name of window and the 2nd the image that we want to show itself
    #plt.imshow(canny) #equivalent of cv2.omshow(canny)
    cv2.waitKey(1)   #this displays the image for a certain amount of milliseconds,so we r setting it to 0 then it'll displays the result window infinitely untill a we press any keyboard keyboard
    #plt.show() #equivalent of cv2 show
