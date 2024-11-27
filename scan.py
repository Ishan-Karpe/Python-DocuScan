from skimage.filters import threshold_local  
import argparse  
import cv2  
import imutils  
import numpy as np  
from transform import four_point_transform

ap = argparse.ArgumentParser() # Create an argument parser object  
ap.add_argument("-i", "--image", required = True, help = "Path to the image to be scanned")
args = vars(ap.parse_args())
# lines 7-10 parse the command line arguments, needing only a single switch, which is the image path to be scannned

# Load and resize image  
image = cv2.imread(args["image"])  
ratio = image.shape[0] / 500.0  
orig = image.copy()  
image = imutils.resize(image, height=500)  

# Convert to grayscale and find edges  
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
gray = cv2.GaussianBlur(gray, (5, 5), 0)  
edged = cv2.Canny(gray, 75, 200)  

print("STEP 1: Edge Detection")  
cv2.imshow("Image", image)  
cv2.imshow("Edged", edged)  
cv2.waitKey(0)  
cv2.destroyAllWindows()  

# Find contours  
cnts = cv2.findContours(edged.copy(), 
                        cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  
cnts = imutils.grab_contours(cnts)  
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]  

screenCnt = None  # why none? if we don't find a contour, we'll know

for c in cnts:  
    peri = cv2.arcLength(c, True)  
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)  
    
    if len(approx) == 4:  
        screenCnt = approx  
        break  

if screenCnt is not None:  
    print("STEP 2: Find contours of paper")  
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)  
    cv2.imshow("Outline", image)  
    cv2.waitKey(0)  
    cv2.destroyAllWindows()  
    
    # Apply perspective transform  
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)  
    
    # Convert to grayscale and apply threshold  
    warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)  
    T = threshold_local(warped_gray, 11, offset=10, method="gaussian")  
    warped = (warped_gray > T).astype("uint8") * 255  
    
    print("STEP 3: Apply perspective transform")  
    
    # Show final results  
    cv2.imshow("Original", imutils.resize(orig, height=650))  
    cv2.imshow("Scanned", imutils.resize(warped, height=650))  
    cv2.waitKey(0)  
    cv2.destroyAllWindows()  
else:  
    print("No document contour found. Please ensure the document edges are clearly visible.")