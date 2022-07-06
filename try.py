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

# plates_path = "C:\\Users\\user\\Desktop\\Project\\25_Mar\\characters\\h\\"

for file in os.listdir(plates_path):
    f = os.path.join(plates_path, file)
    set_file_name(file)
    img = cv2.imread(f, 0)

    img = image_resize(img, width = 480)
    cv2.imshow('org', img)
    cv2.waitKey(0)

    blur = cv2.medianBlur(img,5)
    cv2.imshow("Blur", blur)
    cv2.waitKey(0)

    if np.mean(blur) > 197:
        its = 'bright'
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 11)
    else:
        its = 'dark'
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 87, 13)

    cv2.imshow("thresh ({})".format(its), thresh)
    cv2.waitKey(0)

    # # create rectangular kernel for dilation
    # rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # dilation = cv2.dilate(thresh, rect_kern, iterations=1)
    # cv2.imshow("Dilation1", dilation)
    # cv2.waitKey(0)

    # rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    # erosion = cv2.erode(dilation, rect_kern, iterations=1)
    # cv2.imshow("Erosion for hist", erosion)
    # cv2.waitKey(0)

    # rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # dilation = cv2.dilate(erosion, rect_kern, iterations=1)
    # cv2.imshow("Dilation2", dilation)
    # cv2.waitKey(0)


    os.chdir(output_path)
    imgname = "{}_thresh.jpg".format(get_file_name()[:-4])
    cv2.imwrite(imgname, thresh)