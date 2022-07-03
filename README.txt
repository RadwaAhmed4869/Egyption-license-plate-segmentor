#This is method 1:
#	resize to 480
#	padding 10 pxs
#	using edge detection canny
		(cv2.blur(img, (5,5))
#	roi with magic number
		roi = canny_cropped[int(h/2.5):int(h/1.12), int(5):int(w-10)]
#	draw_hist d_3 then e_5 then d_3
	
	