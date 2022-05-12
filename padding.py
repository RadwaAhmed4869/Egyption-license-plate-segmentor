import cv2
import os

def padding(fpath, outpath, show):
    for file in os.listdir(fpath):
        f = os.path.join(fpath, file) 
        img = cv2.imread(f, 0)
        if show == 1:
            cv2.imshow('orginal', img)
            cv2.waitKey(0)
 
        img = cv2.copyMakeBorder(img, 10,10,10,10, cv2.BORDER_REPLICATE)
        
        if show == 1:
            cv2.imshow('padding', img)

        os.chdir(outpath)
        imgname = "{}".format(file)
        cv2.imwrite(imgname, img)











# from PIL import Image

# image = Image.open("input.jpg")

# right = 5
# left = 5
# top = 5
# bottom = 5

# width, height = image.size

# new_width = width + right + left
# new_height = height + top + bottom

# result = Image.new(image.mode, (new_width, new_height), (0, 0, 255))

# result.paste(image, (left, top))

# result.save('output.jpg')
