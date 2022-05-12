import cv2
import numpy as np
import os
import scipy.ndimage as ndi
from skimage import feature
import matplotlib.pyplot as plt
from skimage import io


def detect_edges(img_path, draw_path, canny_path, show):
    
    for file in os.listdir(img_path):
        f = os.path.join(img_path, file) 
        img = cv2.imread(f, 0)
        if show == 1:
            cv2.imshow('resized', img)
            cv2.waitKey(0)
        # print(img.shape)

        blurred = cv2.blur(img, (5,5))
        if show == 1:
            cv2.imshow('blur', blurred)
            cv2.waitKey(0)

        ## cv2.canny(image_src, high_th, low_th)
        # if the intensity gradient of a pixel > high_th, it is an edge.
        # A pixel is rejected if its intensity gradient < low_th.
        # A pixel has an intensity between low_th & high_th, it is an edge only if it is connected to any other pixel having the value > hign_th.
        sigma = 0.33
        med = np.median(blurred)
        lower = int(max(0, (1.0 - sigma) * med))
        upper = int(min(255, (1.0 + sigma) * med))
        edges = cv2.Canny(blurred, lower, upper)
        # edges = cv2.Canny(blurred, 50, 200)
        if show == 1:
            cv2.imshow('edges', edges)
            cv2.waitKey(0)

        os.chdir(draw_path)
        imgname = "{}".format(file)
        cv2.imwrite(imgname, edges)

        ## find the non-zero min-max coords of canny
        pts = np.argwhere(edges>0)
        y1,x1 = pts.min(axis=0)
        y2,x2 = pts.max(axis=0)
        # print(file)
        # print(lower, upper)
        # print(y1, x1, y2, x2)

        ## crop the region
        cropped = img[y1:y2, x1:x2]
        if show == 1:
            cv2.imshow('crop_canny', cropped)
            cv2.waitKey(0)

        # edges = feature.canny(img, sigma=3)
        # edges = edges.astype('float32')
        # plt.imsave(canny_path+'{}.jpg'.format(file[:len(file)-4]), edges, cmap=plt.cm.gray)
        # edges = cv2.imread("output//canny.jpg")
        os.chdir(canny_path)
        imgname = "{}".format(file)
        cv2.imwrite(imgname, cropped)