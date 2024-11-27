from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

ap = argparse.ArgumentParser() # Create an argument parser object
# add_arguments has 4 parameters: switch, name, required, help
ap.add_argument("-i", "--image", required = True, help = "Path to the image to be scanned")
args = vars(ap.parse_args())
# lines 7-10 parse the command line arguments, needing only a single switch, which is the image path to be scannned

#resizing our image to have a height of 500 pixels
image = cv2.imread(args["image"]) # Load the image
ratio = image.shape[0] / 500.0 # Calculate the ratio of the old height to the new height
orig = image.copy() # Make a copy of the original image
image = imutils.resize(image, height = 500) # Resize the image to have a height of 500 pixels, imutils is for image resizing

# the following will now convert all edges to grayscale mode in order to find the edges

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert the image to grayscale, BGR to gray
gray = cv2.GaussianBlur(gray, (5, 5), 0) # Apply a Gaussian blur to the image to remove high frequency noise
# A gaussian blur is an image filter that removes high frequency noise from the image
edged = cv2.Canny(gray, 75, 200) # Detect edges in the image using the Canny edge detector
# canny is an edge detection operator

# Why are we edge detecting? 
# We want to find the edges of the paper in the image so that we can use these edges to find the contour of the paper

print("STEP 1: Edge Detection")
cv2.imshow("Image", image) # Display the original image
#imshow is a function that displays an image in a window
cv2.imShow("Edged", edged) # Display the edge-detected image
cv2.waitKey(0)
cv2.destroyAllWindows()

# Basically, The edge detection step is used to find the outlines of the objects in the image. Like an outline of a receipt or a piece of paper

