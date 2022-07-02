import cv2
from preprocessing import *
from crop_canny import *
from csv_hist import *
from draw_fig import *
from segment import *
from settings import *

plates_path = "C:\\Users\\user\\Desktop\\Project\\Egyption-license-plate-segmentor\\src\\LP7\\"


def segment_fn(img, show_characters, draw_fig):
    img_resized = resize_padding_fn(img, show=0)
    roi = detect_edges(img_resized, show=0)
    csv_values = draw_hist(roi, invert=1, show=0)
    promn = 8
    if draw_fig == 1:
        fig(csv_values, promn)

    segments = []
    # find_peaks_fn(roi, csv_values, segments, promn, invert=1, debug=0, show=show_characters)

    return segments

# process_multi_img(0)
# img = cv2.imread(plates_path + "243.jpg")
# characters = segment_fn(img, show_characters=1, draw_fig=0)

for file in os.listdir(plates_path):
    f = os.path.join(plates_path, file)
    set_file_name(file)
    img = cv2.imread(f)
    process_multi_img(1)
    characters = segment_fn(img, show_characters=0, draw_fig=0)

