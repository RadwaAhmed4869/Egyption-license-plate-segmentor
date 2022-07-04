import cv2
from imutils import contours
from preprocessing import *
from crop_canny import *
from csv_hist import *
from draw_fig import *
from segment import *
from settings import *

str = "testall\\"
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
    blur = cv2.GaussianBlur(img, (5,5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    erosion = cv2.erode(thresh, rect_kern, iterations=1)
    
    if show == 1:
        cv2.imshow("Erosion for cnt", erosion)
        cv2.waitKey(0)

    cnts = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts, _ = contours.sort_contours(cnts)
    # print("cnts: ", cnts)

    ROI = img
    if debug == 1:
        for c in cnts:
            area = cv2.contourArea(c)
            print("A: ", area)

    for c in cnts:
        area = cv2.contourArea(c)
        # print(area)
        x,y,w,h = cv2.boundingRect(c)
        center_y = y + h/2
        if debug == 1:
            print("center, h/2: ", center_y, height/2)
        if area > 7900 and (w > h) and center_y > height/2:
            ROI = img[y:y+h, x:x+w]
            if show == 1:
                cv2.imshow("before", ROI)
                cv2.waitKey(0)
            p = 5
            ROI = img[y+3*p:y+h-p, x:x+w-p]
            
            return ROI
        else:
            continue

    if (is_multi()):
        print("file:", get_file_name()[:-4])
        return ROI
    else:
        print("no area bigger than the theroshld ##############################")
        return ROI
            

def segment_fn(img, show_characters, draw_fig):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray', img)
    # cv2.waitKey(0)
    img_resized = image_resize(img, width = 480)
    # cv2.imshow('resize', img_resized)
    # cv2.waitKey(0)
    roi = cnt_fn(img_resized, debug=0, show=0)
    
    h, w = roi.shape
    ratio = w/h
    # print("h: {}, w: {} ratio: {}".format( h, w, ratio))

    if show_characters == 1:
        cv2.imshow('roi', roi)
        cv2.waitKey(0)

    csv_values = draw_hist(roi, invert=1, show=0)
    promn = 8
    if draw_fig == 1:
        fig(csv_values, promn)

    segments = []
    find_peaks_fn(roi, csv_values, segments, promn, invert=1, debug=0, show=show_characters)

    return segments

# process_multi_img(0)
# image_name = "113.jpg"
# img = cv2.imread(plates_path + image_name)
# set_file_name(image_name)
# cv2.imshow('org', img)
# cv2.waitKey(0)
# characters = segment_fn(img, show_characters=1, draw_fig=0)

for file in os.listdir(plates_path):
    f = os.path.join(plates_path, file)
    set_file_name(file)
    # print(file)
    img = cv2.imread(f)
    print(file, "w/h: ", img.shape[1]/img.shape[0])
    process_multi_img(1)
    characters = segment_fn(img, show_characters=0, draw_fig=0)
