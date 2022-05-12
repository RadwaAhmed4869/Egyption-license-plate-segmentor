import csv
import os

resized_path = "C:\\Users\\user\\Desktop\\Project\\11_May\\resize\\"
draw_path = "C:\\Users\\user\\Desktop\\Project\\11_May\\draw_canny\\"
canny_output = "C:\\Users\\user\\Desktop\\Project\\11_May\\crop_canny\\"
cropped_path = "C:\\Users\\user\\Desktop\\Project\\11_May\\crop\\"
csvpath = "C:\\Users\\user\\Desktop\\Project\\11_May\\csv\\"
outpath_hist = "C:\\Users\\user\\Desktop\\Project\\11_May\\hist\\"
# segment_results = "C:\\Users\\user\\Desktop\\Project\\11_May\\seg\\"
padding_path = "C:\\Users\\user\\Desktop\\Project\\11_May\\padding\\"


paths = [resized_path, draw_path, canny_output, cropped_path, csvpath, outpath_hist, padding_path]
for path in paths:
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))

# for f in os.listdir(segment_results):
#     os.remove(os.path.join(segment_results, f))