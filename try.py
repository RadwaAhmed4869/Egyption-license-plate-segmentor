import cv2
import numpy as np
from preprocessing import *
from crop_canny import *
from settings import *

plates_path = "C:\\Users\\user\\Desktop\\Project\\Egyption-license-plate-segmentor\\src\\LP7\\"
process_multi_img(0)

img = cv2.imread(plates_path + '57.jpg')

img_resized = resize_padding_fn(img, show=0)
roi = detect_edges(img_resized, show=0)

# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh_img = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for contour in cnts:
    (x,y,w,h) = cv2.boundingRect(contour)
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
    
for cnt in cnts:
    approx = cv2.contourArea(cnt)
    print(approx)

cv2.imshow('image', img)

cv2.imshow('roi', thresh_img)
cv2.waitKey(0)
