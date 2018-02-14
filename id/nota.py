import cv2
import numpy as np

img1 = cv2.imread('partitura1.png')
img2 = cv2.imread('mask.png')

#escala de cinza
img_cinza = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
mask_cinza = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

kernel = np.ones((2, 2),np.uint8)
img_erode = cv2.erode(img_cinza, kernel, iterations = 1)
mask_erode = cv2.erode(mask_cinza, kernel, iterations = 1)

#pega borda
thresh = 175
borda_img = cv2.Canny(img_erode, thresh, thresh*2)
borda_mask = cv2.Canny(mask_erode, thresh, thresh*2)

cv2.imshow('image', borda_img)
cv2.imshow('mascara', borda_mask)

#extract contours
im1, contorno_img, hier_img = cv2.findContours(borda_img, 2, 1)
im2, contorno_mask, hier_mask = cv2.findContours(borda_mask, 2, 1)
cv2.imshow('borda', im2)

#resultado = cv2.matchShapes(im1,im2,1, 0)
resultado = cv2.matchShapes(contorno_img[30],contorno_mask[0],1, 0)

print (resultado)
cv2.waitKey(0)