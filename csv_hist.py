from typing import ClassVar
import numpy as np
import cv2
import os

# fpath = "C:\\Users\\user\\Desktop\\Project\\27_Mar\\seperate\\resized\\"
# outpath_hist = "C:\\Users\\user\\Desktop\\Project\\27_Mar\\seperate\\hist\\"
# csvpath = "C:\\Users\\user\\Desktop\\Project\\27_Mar\\seperate\\csvfiles\\"

# fpath = "C:\\Users\\user\\Desktop\\Project\\27_Mar\\cropped\\"

def write_csv_values(csvpath, fname, vlist):
    os.chdir(csvpath)
    with open(f"{fname[:len(fname)-4]}.csv", 'w') as txtfile:
        txtfile.write("value\n")
        for v in vlist:
            txtfile.write(str(v))
            txtfile.write('\n')

def draw_hist(fpath, csvpath, outpath_hist, invert, show):
    for file in os.listdir(fpath):
        f = os.path.join(fpath, file) 
        gray = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        # print("SHAPE: ", gray.shape)

    # gray = cv2.imread(fpath + 'crop5.jpg', cv2.IMREAD_GRAYSCALE)

        # resize image to three times as large as original for better readability
        # gray = cv2.resize(gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)
        # cv2.imshow("original", gray)
        # cv2.waitKey(0)

        # perform gaussian blur to smoothen image
        blur = cv2.GaussianBlur(gray, (5,5), 0)
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
            cv2.imshow("thresh {}".format(file), thresh)
            cv2.waitKey(0)

        # create rectangular kernel for dilation
        rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        # # apply dilation to make regions more clear
        # erosion = cv2.erode(thresh, rect_kern, iterations=1)
        # cv2.imshow("Erosion", erosion)
        dilation = cv2.dilate(thresh, rect_kern, iterations=1)
        if show == 1:    
            cv2.imshow("Dilation {}".format(file), dilation)
            cv2.waitKey(0)

        binarizedImage = dilation
        # normal mode .. 0 black pixels = 1 (to be counted)
        # inverted mode .. 255 white pixels = 1
        if invert == 0:
            binarizedImage[binarizedImage == 0] = 1
            binarizedImage[binarizedImage == 255] = 0
            
        if invert == 1:
            binarizedImage[binarizedImage == 0] = 0
            binarizedImage[binarizedImage == 255] = 1
        
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
        # sum_columns = np.sum(hist, axis=0)
        # print(values)
        # print(file)

    # write histogram values to a csv file in folder 
        write_csv_values(csvpath, file, values)
        # print("min: ", np.min(values))
        # print("max: ", np.max(values))
        # print("unique values: ", np.unique(values))
        # print("****************************************************************")
        # print("mean: ", np.mean(sum_columns))
        # print("std: ", np.std(sum_columns))

        if show == 1:
            cv2.imshow("vertical histogram {}".format(file), hist)
            cv2.waitKey(0)

    # save histograms to outpath_hist folder
        os.chdir(outpath_hist)
        imgname = "hist{}".format(file)
        cv2.imwrite(imgname, hist)