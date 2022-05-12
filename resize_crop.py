# code to resize and cut the charaters region only
import cv2
import numpy as np
import os

# fpath = "C:\\Users\\user\\Desktop\\Project\\25_Mar\\crop"
# outpath = "C:\\Users\\user\\Desktop\\Project\\25_Mar\\first70resized\\"

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized

def resize_crop_fn(fpath, outpath, crop, show):
    for file in os.listdir(fpath):
        f = os.path.join(fpath, file) 
        img = cv2.imread(f, 0)
        if show == 1:
            cv2.imshow('orginal', img)
            cv2.waitKey(0)

        # w = 170
        # h = 85
        # img = cv2.resize(img, (w, h))
        # img = cv2.resize(img, None, fx=0.5, fy=0.5)
        # bigger = cv2.resize(gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)
        
        if crop == 0:
            img = image_resize(img, width = 480)
            if show == 1:
                cv2.imshow('resized', img)
                cv2.waitKey(0)

        h, w = img.shape
        # crop image initail height:final height, initail width:final width
        # this the crop I used to do before canny, now ignore it
        if crop == 1:
            img = img[int(h/2.5):int(h/1.12), int(5):int(w-10)]
            if show == 1:
                cv2.imshow('crop', img)
                cv2.waitKey(0)

        # print(img.shape)
        os.chdir(outpath)
        imgname = "{}".format(file)
        cv2.imwrite(imgname, img)