# 11/27/2024

from skimage.filters import threshold_local  
import argparse  
import cv2  
import imutils  
from transform import four_point_transform

ap = argparse.ArgumentParser() # Create an argument parser object  
ap.add_argument("-i", "--image", required = True, help = "Path to the image to be scanned")
args = vars(ap.parse_args())
# --image is the path to the image we want to scan, included in the prompt to launch the script
# lines 7-10 parse the command line arguments, needing only a single switch, which is the image path to be scannned
# add_argument() method is used to define the command line arguments that the script will accept
# Load and resize image  
image = cv2.imread(args["image"])  
#imread is used a lot in OpenCV to load images
ratio = image.shape[0] / 500.0  
# the ratio will allow us to resize the image to a height of 500 pixels
orig = image.copy()  
# we are performing the scan on the orginal image, so we need to make a copy of it

image = imutils.resize(image, height=500)  

# Convert to grayscale and find edges  
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
gray = cv2.GaussianBlur(gray, (5, 5), 0)  
edged = cv2.Canny(gray, 75, 200)  
# A guassian blur is applied to the image to remove high frequency noise
# Canny edge detection is then applied to find the edges in the image

print("STEP 1: Edge Detection")  
cv2.imshow("Image", image)  
cv2.imshow("Edged", edged)  
cv2.waitKey(0)  
cv2.destroyAllWindows()  
# when the user clicks a key, the windows will be destroyed, and the next process will begin


# Find contours  
cnts = cv2.findContours(edged.copy(), 
                        cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  
cnts = imutils.grab_contours(cnts)  
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]  

screenCnt = None  # why none? if we don't find a contour, we'll know

for c in cnts:  
    peri = cv2.arcLength(c, True)  
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)  
    
    #arcLength() is used to compute the perimeter
    #approxPolyDP() is used to approximate the shape of the contour
    # loop over the contours to find the document in the image also approxiamte the contour
    
    
    if len(approx) == 4:  # if the length of the approximated contour is 4, then we have found the document

        screenCnt = approx  
        break  

if screenCnt is not None:  #if it is none, then we have not found the document
    print("STEP 2: Find contours of paper")  
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)  
    #screencnt was a problem at first, drawContours() is used to draw the contours of the document
    cv2.imshow("Outline", image)  
    cv2.waitKey(0)  
    cv2.destroyAllWindows()  
    # again, the windows will be destroyed when the user clicks a key
    
    # Apply perspective transform  
    # the following is achieved from the transform.py file
    # the transform.py was copy pasted as it is a custom module that is not part of pyhton's standard library
    
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)  
    
    # Convert to grayscale and apply threshold  
    warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)  
    T = threshold_local(warped_gray, 11, offset=10, method="gaussian")  
    warped = (warped_gray > T).astype("uint8") * 255  
    # perspecive is the main part of the scan, it is the transformation of the document to a top-down view
    # threshold_local() is used to apply thresholding to the scanned document
    # four parameters are passed to the threshold_local() function
    # grayscale image, block size, offset, and method
    print("STEP 3: Apply perspective transform")  
    
    # Show final results  
    cv2.imshow("Original", imutils.resize(orig, height=650))  
    cv2.imshow("Scanned", imutils.resize(warped, height=650))  
    # things are reiszied to make them easier to view, also a black and white feel. 
    cv2.waitKey(0)  
    cv2.destroyAllWindows()  
else:  
    print("No document contour found. Please ensure the document edges are clearly visible.")
# if the document is not found, the user will be notified


"""In Summary:

A contour is a curve joining all the points (along the boundary).
Contours are useful for shape analysis and object detection and recognition.

Edge detection is used to find the boundaries of objects within an image.

1. Load the image and resize it to a reasonable size
2. Convert the image to grayscale and find the edges
3. Find the contours in the edged image
4. Approximate the contour of the document
5. Apply a perspective transform to obtain a top-down view of the document

NOTE: this also works with peices of paper, not just documents.
"""