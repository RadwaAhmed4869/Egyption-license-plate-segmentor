import cv2
from driver_code import *

image_name = "88.jpg"
img = cv2.imread(plates_path + image_name)
characters = segment_fn(img, debug=0, show_characters=0, draw_fig=0, multi=0)


# for file in os.listdir(plates_path):
#     f = os.path.join(plates_path, file)
#     set_file_name(file)
#     print("----------------------------------------------")
#     print(file)
#     img = cv2.imread(f)
#     # cv2.imshow('org', img)
#     # cv2.waitKey(0)
#     # print(file, "w/h: ", img.shape[1]/img.shape[0])
#     characters = segment_fn(img, debug=1, show_characters=0, draw_fig=0, multi=1)