## canny for edge detection method (discarded):
	resize to 480
	padding 10 pxs
	using edge detection canny
		(cv2.blur(img, (5,5))
	roi with magic number
		roi = canny_cropped[int(h/2.5):int(h/1.12), int(5):int(w-10)]
	draw_hist d_3 then e_5 then d_3
	
# Find-contour method:
## (find-contour branch merged with main)

	resize input image to 480 (the output of the detector either near or far)
	get the roi with cnt_fn(img)
		cv2.GaussianBlur(img, (5,5), 0)
		cv2.threshold()
		then erode with 7 kernal
	cnts = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	here, the code split into two approaches:
###	1.
	    cnts, _ = contours.sort_contours(cnts, method="left-to-right")
		choose the roi depending of 3 IFs:
        if area > 8000 and (w > h) and center_y > height/2:

###	2. 
		cnts, _ = contours.sort_contours(cnts)
    	cntsSorted = sorted(cnts, key=lambda x: cv2.contourArea(x))
		select roi depending on largest contour:
    	selected_contour = cntsSorted[-1]
