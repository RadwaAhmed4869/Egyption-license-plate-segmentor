import numpy as np
import cv2
import os
from settings import * 

def draw_hist(img, invert, show):
    blur = cv2.GaussianBlur(img, (5,5), 0)
    if show == 1:
        cv2.imshow("Blur", blur)
        cv2.waitKey(0)

    if np.mean(blur) > 197:
        its = 'bright'
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 11)
    else:
        its = 'dark'
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 87, 13)
    if show == 1:    
        cv2.imshow("thresh ({})".format(its), thresh)
        cv2.waitKey(0)

    # create rectangular kernel for dilation
    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # # apply dilation to make regions more clear
    # erosion = cv2.erode(thresh, rect_kern, iterations=1)
    # cv2.imshow("Erosion", erosion)
    dilation = cv2.dilate(thresh, rect_kern, iterations=1)
    if show == 1:    
        cv2.imshow("Dilation", dilation)
        cv2.waitKey(0)

    # os.chdir(outpath_thresh)
    # imgname = "{}".format(file)
    # cv2.imwrite(imgname, dilation)

    binarizedImage = dilation
    # normal mode .. 0 black pixels = 1 (to be counted)
    # inverted mode .. 255 white pixels = 1
    if invert == 0:
        binarizedImage[binarizedImage == 0] = 1
        binarizedImage[binarizedImage == 255] = 0
        
    if invert == 1:
        binarizedImage[binarizedImage == 0] = 0
        binarizedImage[binarizedImage == 255] = 1

    # if show == 1:
    #     binarizedImage[binarizedImage == 0] = 1
    #     binarizedImage[binarizedImage == 1] = 0
    #     cv2.imshow("{}".format(file), binarizedImage)
    #     cv2.waitKey(0)
    
    vertical_projection = np.sum(binarizedImage, axis=0)
    # print(vertical_projection)

    height, width = binarizedImage.shape
    # print('width : ', width)
    # print('height : ', height)

    blankImage = np.zeros((height, width, 3), np.uint8)
    # print(blankImage)

    values = []

    for column in range(width):
        # print(column)
        cv2.line(blankImage, (column, 0), (column, int(vertical_projection[column]*height/width)), (255,255,255), 1)
        values.append(int(vertical_projection[column]*height/width))
        # print(int(vertical_projection[column]*height/width))

    hist = cv2.flip(blankImage, 0)
    if(is_multi()):
        os.chdir(output_path)
        imgname = "{}_hist.jpg".format(get_file_name()[:-4])
        cv2.imwrite(imgname, hist)
    # sum_columns = np.sum(hist, axis=0)
    # print(values)
    # print(file)

# write histogram values to a csv file in folder 
    # write_csv_values(csvpath, file, values)
    # print("min: ", np.min(values))
    # print("max: ", np.max(values))
    # print("unique values: ", np.unique(values))
    # print("****************************************************************")
    # print("mean: ", np.mean(sum_columns))
    # print("std: ", np.std(sum_columns))

    # if show == 1:
    #     cv2.imshow("vertical histogram {}".format(file), hist)
    #     cv2.waitKey(0)

    return values