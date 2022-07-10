from imutils import contours
from preprocessing import *
from crop_canny import *
from csv_hist import *
from draw_fig import *
from segment import *
from settings import *
from preprocessing import *


def cnt_fn(img, show):
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

    ROI = img

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
        return ROI

    print("conditions to crop ROI are not satisfied")
    return ROI

def segment_fn(img, debug, show_characters, draw_fig, multi):
    process_multi_img(multi)

    segments = []

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    roi = cnt_fn(img, show=0)
    h, w = roi.shape
    if is_multi == 1:
        print("---------------------------------")
        print(get_file_name()[:-4])
        # print("h: {}, w: {}".format( h, w))

    if w < 54:
        if debug == 1:
            print("< 54")
            print("This frame was skipped")
            print("----------------------------------------------")
        return segments

    if w >= 237:
        if debug == 1:
            print(">= 237")
            print("This frame was skipped")
            print("----------------------------------------------")

        return segments

    ratio = w/h
    # print("h: {}, w: {}, ratio: {}".format( h, w, ratio))

    if ratio <= 1.6:
        if debug == 1:
            print("< 1.6")
            print("This frame was skipped")
            print("----------------------------------------------")
        return segments

    roi_resized = image_resize(roi, width = 480)
    csv_values = draw_hist(roi_resized, invert=1, show=0)
    promn = 8
    if draw_fig == 1:
        fig(csv_values, promn)

    find_peaks_fn(roi_resized, csv_values, segments, promn, invert=1, debug=0, show=show_characters)
    
    print("frame segmented successfully")
    print("----------------------------------------------")

    return segments