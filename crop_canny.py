import cv2
import os
import numpy as np
from settings import *

def detect_edges(img, show):
    # blur = cv2.medianBlur(img,5)
    # blurred = cv2.GaussianBlur(img, (5,5), 0)
    blurred = cv2.blur(img, (5,5))
    sigma = 0.33
    med = np.median(blurred)
    lower = int(max(0, (1.0 - sigma) * med))
    upper = int(min(255, (1.0 + sigma) * med))
    edges = cv2.Canny(blurred, lower, upper)
    # edges = cv2.Canny(blurred, 50, 200)
    if show == 1:
        cv2.imshow('edges', edges)
        cv2.waitKey(0)

    if(is_multi()):
        os.chdir(output_path)
        imgname = "{}_edges.jpg".format(get_file_name()[:-4])
        cv2.imwrite(imgname, edges)

    ## find the non-zero min-max coords of canny
    pts = np.argwhere(edges>0)
    y1,x1 = pts.min(axis=0)
    y2,x2 = pts.max(axis=0)
    # print(file)
    # print(lower, upper)
    # print(y1, x1, y2, x2)

    ## crop the region
    canny_cropped = img[y1:y2, x1:x2]
    if show == 1:
        cv2.imshow('crop_canny', canny_cropped)
        cv2.waitKey(0)

    h, w = canny_cropped.shape
    # crop the 2/3 lower part of the image (region of interest)
    roi = canny_cropped[int(h/2.5):int(h/1.12), int(5):int(w-10)]
    if show == 1:
        cv2.imshow('roi', roi)
        cv2.waitKey(0)

    # if(is_multi()):
    #     os.chdir(output_path)
    #     imgname = "{}_roi.jpg".format(get_file_name()[:-4])
    #     cv2.imwrite(imgname, roi)
        
    return roi