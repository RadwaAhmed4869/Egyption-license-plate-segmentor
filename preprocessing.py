import cv2
import os
from settings import * 

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the original image
    if width is None and height is None:
        return image

    if width is None:
        # calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation = inter)
    return resized

def resize_padding_fn(img, show):
    if show == 1:
        cv2.imshow("original", img)
        cv2.waitKey(0)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = image_resize(img, width = 480)
    if show == 1:
        cv2.imshow('resized', img)
        cv2.waitKey(0)

    # padding
    img = cv2.copyMakeBorder(img, 10,10,10,10, cv2.BORDER_REPLICATE)
    
    if show == 1:
        cv2.imshow('padding', img)
        cv2.waitKey(0)

    result = img

    if(is_multi()):
        os.chdir(output_path)
        imgname = "{}_padding.jpg".format(get_file_name()[:-4])
        cv2.imwrite(imgname, result)

    return result