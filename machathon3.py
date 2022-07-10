from types import GeneratorType
import cv2
import os
from draw_fig import *

# Machathon3.py is used to segment (better cut) the charaters that were cut by the bounding boxes
name = "Y\\"
input_path = "C:\\Users\\user\\Desktop\\Project\\machathon3_input\\" + name
output_path = "C:\\Users\\user\\Desktop\\Project\\macathon3_output\\" + name

def process_multi_img(set):
    global multi 
    multi = set

def is_multi():
    return multi

def set_file_name(filename):
    global file_name
    file_name = filename

def get_file_name():
    return file_name


def draw_hist(img, invert, show):
    blur = cv2.medianBlur(img,5)
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
    dilation = cv2.dilate(thresh, rect_kern, iterations=1)
    if show == 1:    
        cv2.imshow("Dilation1", dilation)
        cv2.waitKey(0)

    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    erosion = cv2.erode(dilation, rect_kern, iterations=1)
    if show == 1:    
        cv2.imshow("Erosion for hist", erosion)
        cv2.waitKey(0)

    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilation = cv2.dilate(erosion, rect_kern, iterations=1)
    if show == 1:    
        cv2.imshow("Dilation2", dilation)
        cv2.waitKey(0)

    
    binarizedImage = dilation
        
    if invert == 1:
        binarizedImage[binarizedImage == 0] = 0
        binarizedImage[binarizedImage == 255] = 1

    vertical_projection = np.sum(binarizedImage, axis=0)


    height, width = binarizedImage.shape

    blankImage = np.zeros((height, width, 3), np.uint8)

    values = []

    for column in range(width):
        cv2.line(blankImage, (column, 0), (column, int(vertical_projection[column]*height/width)), (255,255,255), 1)
        values.append(int(vertical_projection[column]*height/width))

    return values


def segment_invert(img, peak, segments, debug, show):
    height, width = img.shape
    if debug == 1:
        print("ROI wth = {},".format(width))
    for v in range(len(peak)-1):
        p = 0
        char = img[int(0):, int(peak[v]+p):int(peak[v+1]-p)]

        if (char.shape[1] < 2):
            if debug == 1:
                print("{}_{}.jpg".format(get_file_name()[:-4], v+1), "char width:", char.shape[1])
            continue

        if(is_multi()):
            os.chdir(output_path)
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
        print(get_file_name()[:-4], " - zero peaks")

    copy = img
    for i in indices:
        cv2.line(copy, (i, 0), (i, int(height)), (0, 255, 0), 1)

    small_peaks = np.where(indices < 2)
    indices = np.delete(indices, small_peaks)

    if show == 1:
        cv2.imshow("lines at peaks", copy)
        cv2.waitKey(0)

    # if(is_multi()):
    #     os.chdir(output_path)
    #     imgname = "{}_lines of peaks.jpg".format(get_file_name()[:-4])
    #     cv2.imwrite(imgname, copy)

    if invert == 1:
        if debug == 1:
            # print("w=", img.shape[1])
            print("Peak indices: ", list(indices))
        segment_invert(img, indices, segments, debug, show)


def fn(img, draw_fig=0):

    segments = []
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    csv_values = draw_hist(img, invert=1, show=0)
    promn = 13
    if draw_fig == 1:
        fig(csv_values, promn)

    find_peaks_fn(img, csv_values, segments, promn, invert=1, debug=0, show=0)
    return segments

# process_multi_img(0)
# image_name = "1656869288.397192_L.jpg_cropped.jpg"
# img = cv2.imread(input_path + image_name)
# set_file_name(image_name)

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# os.chdir(output_path)
# imgname = "{}_char_{}.jpg".format(get_file_name()[:-4], "1")
# cv2.imwrite(imgname, gray)

# cv2.imshow('org', img)
# cv2.waitKey(0)

# character = fn(img)

process_multi_img(1)
for file in os.listdir(input_path):
    f = os.path.join(input_path, file)
    set_file_name(file)
    img = cv2.imread(f)
    # cv2.imshow('org', img)
    # cv2.waitKey(0)
    character = fn(img)