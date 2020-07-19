import cv2
import numpy as np

cam = cv2.VideoCapture(0)
cv2.namedWindow("main")
cv2.namedWindow("extra")

while True:
	ret, frame = cam.read()

	output = frame.copy()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray_blurred = cv2.blur(gray, (3, 3))

	# Apply Hough transform on the blurred image.
	detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=1, maxRadius=40)

	# Draw circles that are detected.
	if detected_circles is not None:
		detected_cicles = detected_circles[:80] # cap at 80 detections

		# Convert the circle parameters a, b and r to integers.
		detected_circles = np.uint16(np.around(detected_circles))

		for pt in detected_circles[0, :]:
			a, b, r = pt[0], pt[1], pt[2]

			# Draw the circumference of the circle.
			cv2.circle(output, (a, b), r, (0, 255, 0), 2)
			# Draw a small circle (of radius 1) to show the center.
			cv2.circle(output, (a, b), 1, (0, 0, 255), 3)

			# cut out interior of circle
			height, width, _ = frame.shape
			mask = np.zeros((height, width), np.uint8)

			# draw on mask
			cv2.circle(mask, (a, b), r, (255, 255, 255), thickness=-1)

			# copy image using mask
			masked_data = cv2.bitwise_and(frame, frame, mask=mask)

			# apply threshold
			_, thresh = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

			# find contours
			contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
			x, y, w, h = cv2.boundingRect(contours[0])

			crop = masked_data[y:y+h, x:x+w]

			cv2.imshow("extra", crop)

			# ensure uniform color distribution in circle
			for pixel in masked_data:
				# print(pixel)
				pass

	cv2.imshow("main", output)

	# -- state validation
	# TODO: contour match vials to know how many bubbles we should be looking for
	# check for all circles with uniform color inside
	# make sure there are two of each color

	k = cv2.waitKey(1)
	if k%256 == 27:
		# ESC pressed
		print("Escape hit, closing...")
		break

cam.release()
cv2.destroyAllWindows()