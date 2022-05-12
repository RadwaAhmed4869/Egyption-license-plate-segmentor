from ast import And
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import os
import cv2


# function to segment the image
# takes 3 parameters: the image, list of start indecies, list of end indices
def segment(img, start, peak, end, img_name, outpath, show):
    for v in range(len(start)):
        # print(start[v], end[v])

# if the start index is less than 5, crop from the start index, otherwise move -7 pixels
# I had to do this because one image started from 3
        if start[v] < 7:
            s = 0
        else:
            s = 7

        # initial_width = int(start[v]-s)
        # final_width = int(end[v]+7)
        char = img[int(0):, int(start[v]-s):int(end[v]+7)]

        height, width = img.shape
        # print(final_width-initial_width)
        # if (final_width-initial_width <= 32):
        #     print("less than")
        if (peak[v] <= width/1.9):
            # print("in center 1")
            if (peak[v] >= width/2.19):
                # print("line deleted!")
                continue

# move to the output directry to save cropped images
        os.chdir(outpath)
        dir = os.path.join(outpath, img_name)
        if not os.path.exists(dir):
            os.mkdir(dir)
        os.chdir(dir)
        part_name = "{}_{}.jpg".format(img_name, v+1)
        if show == 1:
            print(part_name)
            cv2.imshow('char{}'.format(v+1), char)
            cv2.waitKey(0)
            
        cv2.imwrite(part_name, char)

def find_peaks_fn(impath, csvpath, outpath, invert, show):
    # loop over the csv files to get the data of the histograms
    for csvfile in os.listdir(csvpath):
        f = os.path.join(csvpath, csvfile)
        # print(csvfile)

        data = pd.read_csv(f)
        hist = data['value']
        # print(hist)
        # print(data.shape)
        # print(time_series.shape)

    # smooth the data
        kernel_size = 5
        kernel = np.ones(kernel_size) / kernel_size
        hist = np.convolve(hist, kernel, mode='same')

        indices = find_peaks(hist, prominence=7)[0]
        
        if indices.size == 0:
            print(csvfile, "zero peaks")
        # print(indices)
        small_peaks = np.where(indices < 5)
        indices = np.delete(indices, small_peaks)
        # print(indices)


    # start and end lists to save the start and end indices
        startix = []
        endix = []

        img = cv2.imread(impath + csvfile[:len(csvfile)-4]+'.jpg', cv2.IMREAD_GRAYSCALE)
        # print(img)
        # print("what I get: ", impath + csvfile[:len(csvfile)-4]+'.jpg')
        # cv2.imshow('img taken', img)
        # cv2.waitKey(0)

        # print(img.shape)
        height, width = img.shape
        lowest_value = 2.5

        if invert == 0:
            for index in indices:
        # get the start index
                temp_index = index-2
                while(temp_index) > 0:
                    if temp_index <= 2:
                        startix.append(1)
                        break

                    elif hist[temp_index] <= lowest_value:
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

                    elif hist[temp_index] <= lowest_value:
                        endix.append(temp_index)
                        break
                    else:
                        temp_index = temp_index+2
                    
        if invert == 1:
            segment

        print(csvfile)
        print("Start indices: ", startix)
        print("Peak indices: ", list(indices))
        print("End indices: ", endix)

        # print("start, peak, end", len(startix), len(indices), len(endix))

        # cv2.imshow('img to segment', img)
        # cv2.waitKey(0)
        # check if start, peak and end indices have the same length
        if(len(startix) != len(indices) or len(indices) != len(endix) or len(startix) != len(endix)):
            print("not matching dim")
        elif invert == 0:
            # print('match!')
            # print(csvfile[:len(csvfile)-4]+'.jpg')

    # segment the image only if the indices match
            segment(img, startix, indices, endix, csvfile[:len(csvfile)-4], outpath, show)
        # elif invert == 1:
        #     segment_invert(img, indices, csvfile[:len(csvfile)-4], outpath, show)