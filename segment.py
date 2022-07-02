from ast import And
# from distutils.log import debug
# import plotly.graph_objects as go
import numpy as np
from scipy.signal import find_peaks
import os
import cv2
import numpy as np
from settings import *

# function to segment the image
# takes 3 parameters: the image, list of start indecies, list of end indices
def segment(img, start, peak, end, segments, show):
    for v in range(len(start)):
        # print(start[v], end[v])

# if the start index is less than 5, crop from the start index, otherwise move -5 pixels
# I had to do this because one image started from 3
        if start[v] < 7:
            s = 0
        else:
            s = 7

        initial_width = int(start[v]-s)
        final_width = int(end[v]+7)
        # print(initial_width, final_width)
        char = img[int(0):, initial_width:final_width]

        height, width = img.shape
        # print("WIDTH: ", width)
        # print("###")
        # print(final_width-initial_width)
        # if (final_width-initial_width <= 32):
        #     print("less than")
        if (peak[v] <= width/1.9):
            # print("in center 1")
            if (peak[v] >= width/2.19):
                print("line deleted!")
                continue
    
        if show == 1:
            cv2.imshow("char_{}".format(v+1), char)
            cv2.waitKey(0)
        
        segments.append(char)
        # segments = np.append(segments, img[int(0):, int(start[v]-s):int(end[v]+7)], axis=0)

def segment_invert(img, peak, segments, debug, show):

    for v in range(len(peak)-1):

        height, width = img.shape
        # print(final_width-initial_width)
        # if (final_width-initial_width <= 32):
        #     print("less than")
        if (peak[v+1] <= width/1.72):
            # print("in center 1")
            if (peak[v] >= width/2.4):
                if debug == 1:
                    print("img wth = {},".format(width), "center line deleted")
                continue

        char = img[int(0):, int(peak[v]+5):int(peak[v+1]-5)]
        if (char.shape[1] < 20):
            # print("{}_{}.jpg".format(img_name, v+1), "char width:", char.shape[1])
            continue

        if np.mean(char) > 197:
            its = 'bright'
            char = cv2.adaptiveThreshold(char, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 11)
        else:
            its = 'dark'
            char = cv2.adaptiveThreshold(char, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 87, 13)

        if(is_multi()):
            os.chdir(char_path)
            folder = "{}".format(get_file_name()[:-4])
            path = os.path.join(char_path, folder)
            isExist = os.path.exists(path)
            if not isExist:
                os.mkdir(path)
            os.chdir(path)
            imgname = "{}_char_{}.jpg".format(get_file_name()[:-4], v+1)
            cv2.imwrite(imgname, char)

        if show == 1:
            if(is_multi()):
                cv2.imshow("{}_char_{}{}.jpg".format(get_file_name()[:-4],its, v+1), char)
                cv2.waitKey(0)
            else:
                cv2.imshow("char_{}".format(v+1), char)
                cv2.waitKey(0)
        segments.append(char)


def find_peaks_fn(img, csv_values, segments, promn, invert, debug, show):
    # print(img.shape)
    height, width,= img.shape

    hist = csv_values

# smooth the data
    kernel_size = 5
    kernel = np.ones(kernel_size) / kernel_size
    hist = np.convolve(hist, kernel, mode='same')

    indices = find_peaks(hist, prominence=promn)[0]

    if indices.size == 0:
        print(get_file_name()[:-4], " - zero peaks")

    copy = img
    for i in indices:
        cv2.line(copy, (i, 0), (i, int(height)), (0, 255, 0), 1)
    small_peaks = np.where(indices < 5)
    indices = np.delete(indices, small_peaks)
    # print(indices)

    if show == 1:
        cv2.imshow("lines at peaks", copy)
        cv2.waitKey(0)

    if(is_multi()):
        os.chdir(output_path)
        imgname = "{}_lines of peaks.jpg".format(get_file_name()[:-4])
        cv2.imwrite(imgname, copy)



# start and end lists to save the start and end indices
    startix = []
    endix = []

    lowest_value = 2.5

    if invert == 0:
        for index in indices:
    # get the start index
            temp_index = index-2
            while(temp_index) > 0:
                if temp_index <= 2:
                    startix.append(1)
                    break

                elif hist[temp_index] < lowest_value:
                    startix.append(temp_index)
                    break
                else:
                    temp_index = temp_index-2
    #get the end index
            temp_index = index+2
            while(temp_index) < width:
                if temp_index >= width-2:
                    endix.append(width-1)
                    break

                elif hist[temp_index] < lowest_value:
                    endix.append(temp_index)
                    break
                else:
                    temp_index = temp_index+2

    
    if invert == 0:
        if debug == 1:
            print("Start indices: ", startix)
            print("Peak indices: ", list(indices))
            print("End indices: ", endix)

        if(len(startix) != len(indices) or len(indices) != len(endix) or len(startix) != len(endix)):
            print("not matching dim")
        else:
            # print('match!')
            # print(csvfile[:len(csvfile)-4]+'.jpg')

    # segment the image only if the indices match
            segment(img, startix, indices, endix, segments, show)

    if invert == 1:
        if debug == 1:
            # print("w=", img.shape[1])
            print(get_file_name())
            print("Peak indices: ", list(indices))
        segment_invert(img, indices, segments, debug, show)