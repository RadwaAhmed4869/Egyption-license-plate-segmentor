import cv2
from imutils import contours
from preprocessing import *
from crop_canny import *
from csv_hist import *
from draw_fig import *
from segment import *
from settings import *

str = "H\\"
plates_path = "C:\\Users\\user\\Desktop\\Project\\Egyption-license-plate-segmentor\\src\\" + str


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

def cnt_fn(img, debug, show):
    # print(img.shape)
    height, width = img.shape
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(img, (5,5))
    # blur = cv2.GaussianBlur(img, (5,5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    k = 5
    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (k,k))
    erosion = cv2.erode(thresh, rect_kern, iterations=1)
    
    if show == 1:
        cv2.imshow("Erosion for cnt", erosion)
        cv2.waitKey(0)

    cnts = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts, _ = contours.sort_contours(cnts)
    cntsSorted = sorted(cnts, key=lambda x: cv2.contourArea(x))
    # print("cnts: ", cnts)

    ROI = img
    # if debug == 1:
    #     for c in cntsSorted:
    #         area = cv2.contourArea(c)
    #         print("A: ", area)

    # select largest contour
    selected_contour = cntsSorted[-1]
    area = cv2.contourArea(selected_contour)
    # print(area)
    x,y,w,h = cv2.boundingRect(selected_contour)
    center_y = y + h/2
    # if debug == 1:
    #     print("center, h/2: ", center_y, 2*height/3)
    if (w > h):
        ROI = img[y:y+h, x:x+w]
        # if show == 1:
        #     cv2.imshow("before", ROI)
        #     cv2.waitKey(0)
        # p = 5
        # ROI = img[y+p:y+h-p, x:x+w-p]
        
        return ROI

    # print("file:", get_file_name()[:-4])
    print("conditions are not satisfied ##############################")
    return ROI

def segment_fn(img, show_characters, draw_fig):
    segments = []
    # print(len(segments))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray', img)
    # cv2.waitKey(0)
    # img_resized = image_resize(img, width = 480)
    # cv2.imshow('resize', img_resized)
    # cv2.waitKey(0)
    roi = cnt_fn(img, debug=1, show=0)
    h, w = roi.shape
    print("---------------------------------")
    print(get_file_name()[:-4])
    # print("h: {}, w: {}".format( h, w))

    if w < 54:
        print("< 54")
    #     return segments

    if w >= 237:
        print(">= 237")
    #     return segments

    ratio = w/h
    print("h: {}, w: {}, ratio: {}".format( h, w, ratio))

    if ratio <= 1.6:
        print("< 1.6")
    #     return segments

    roi_resized = image_resize(roi, width = 480)

    if show_characters == 1:
        cv2.imshow('roi_resized', roi_resized)
        cv2.waitKey(0)

    csv_values = draw_hist(roi_resized, invert=1, show=0)
    promn = 8
    if draw_fig == 1:
        fig(csv_values, promn)

    find_peaks_fn(roi_resized, csv_values, segments, promn, invert=1, debug=0, show=show_characters)

    return segments

# process_multi_img(0)
# image_name = "151.jpg"
# img = cv2.imread(plates_path + image_name)
# set_file_name(image_name)
# cv2.imshow('org', img)
# cv2.waitKey(0)
# characters = segment_fn(img, show_characters=1, draw_fig=0)
# if len(characters) == 0:
#     print("### skipped ###")

for file in os.listdir(plates_path):
    f = os.path.join(plates_path, file)
    set_file_name(file)
    # print("----------------------------------------------")
    # print(file)
    img = cv2.imread(f)
    # cv2.imshow('org', img)
    # cv2.waitKey(0)
    # print(file, "w/h: ", img.shape[1]/img.shape[0])
    process_multi_img(1)
    characters = segment_fn(img, show_characters=0, draw_fig=0)
    if len(characters) == 0:
        print("### skipped ###")
