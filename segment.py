from ast import And
# from distutils.log import debug
# import plotly.graph_objects as go
import numpy as np
from scipy.signal import find_peaks
import os
import cv2
import numpy as np
from settings import *

def segment_invert(img, peak, segments, debug, show):
    height, width = img.shape
    if debug == 1:
        print("ROI wth = {},".format(width))
    for v in range(len(peak)-1):
        # print(final_width-initial_width)
        # if (final_width-initial_width <= 32):
        #     print("less than")
        if (peak[v+1] <= width/1.72):
            # print("in center 1")
            if (peak[v] >= width/2.4):
                if debug == 1:
                    print(get_file_name()[:-4], "ROI wth = {},".format(width), "center line deleted")
                    print("{}_char_{}.jpg".format(get_file_name()[:-4], v+1))
                continue
        p = 0
        char = img[int(0):, int(peak[v]+p):int(peak[v+1]-p)]
        # print(char.shape[1])

        if (char.shape[1] < 2):
            if debug == 1:
                print("{}_{}.jpg".format(get_file_name()[:-4], v+1), "char width:", char.shape[1])
            continue

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
                cv2.imshow("{}_char_{}.jpg".format(get_file_name()[:-4], v+1), char)
                cv2.waitKey(0)
            else:
                cv2.imshow("char_{}".format(v+1), char)
                cv2.waitKey(0)
        segments.append(char)

def find_peaks_fn(img, csv_values, segments, promn, invert, debug, show):
    height, width,= img.shape
    hist = csv_values

# smooth the data
    kernel_size = 5
    kernel = np.ones(kernel_size) / kernel_size
    hist = np.convolve(hist, kernel, mode='same')

    indices = find_peaks(hist, prominence=promn)[0]

    if indices.size == 0:
        if is_multi:
            print(get_file_name()[:-4], " - zero peaks")
        else:
            print("zero peaks")

    copy = img
    for i in indices:
        cv2.line(copy, (i, 0), (i, int(height)), (0, 255, 0), 1)

    # print(indices)
    small_peaks = np.where(indices < 2)
    indices = np.delete(indices, small_peaks)
    # print(indices)

    if show == 1:
        cv2.imshow("lines at peaks", copy)
        cv2.waitKey(0)

    if(is_multi()):
        os.chdir(output_path)
        imgname = "{}_lines of peaks.jpg".format(get_file_name()[:-4])
        cv2.imwrite(imgname, copy)

    if invert == 1:
        if debug == 1:
            # print("w=", img.shape[1])
            print("Peak indices: ", list(indices))
        segment_invert(img, indices, segments, debug, show)