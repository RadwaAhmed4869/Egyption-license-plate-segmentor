from detect_edge import detect_edges
from resize_crop import *
from csv_hist import *
from segment import *
from padding import *
import cv2

plates_path = "C:\\Users\\user\\Desktop\\Project\\11_May\\src\\test2\\"
resized_path = "C:\\Users\\user\\Desktop\\Project\\11_May\\resize\\"

padding_path = "C:\\Users\\user\\Desktop\\Project\\11_May\\padding\\"

draw_path = "C:\\Users\\user\\Desktop\\Project\\11_May\\draw_canny\\"
canny_output = "C:\\Users\\user\\Desktop\\Project\\11_May\\crop_canny\\"

cropped_path = "C:\\Users\\user\\Desktop\\Project\\11_May\\crop\\"
csvpath = "C:\\Users\\user\\Desktop\\Project\\11_May\\csv\\"
outpath_hist = "C:\\Users\\user\\Desktop\\Project\\11_May\\hist\\"
segment_results = "C:\\Users\\user\\Desktop\\Project\\11_May\\seg2-inverted\\"


resize_crop_fn(plates_path, resized_path, crop=0, show=0)
padding(resized_path, padding_path, show=0)
detect_edges(padding_path, draw_path, canny_output, show=0)
resize_crop_fn(canny_output, cropped_path, crop=1, show=0)
# for normal mode ... invert = 0
draw_hist(cropped_path, csvpath, outpath_hist, invert=1, show=1)
find_peaks_fn(cropped_path, csvpath, segment_results, invert=1, show=0)