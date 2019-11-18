import cv2
import sys, os

src = '/home/ti/Downloads/FindFace/FindFace/application/static/folders/second/IMAGE_20190918_112257.jpg'
img = cv2.imread(src)
print('Original Dimensions : ',img.shape)
 
scale_percent = 10 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
 
print('Resized Dimensions : ',resized.shape)
 
cv2.imshow("Resized image", resized)
cv2.imwrite('resized_1.jpg', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()