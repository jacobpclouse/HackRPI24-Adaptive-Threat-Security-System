import cv2
from gunDetection import detect

cam = cv2.VideoCapture(1)

if not cam.isOpened():
    print("Error: Could not open camera.")
    exit(1)

while True:
	ret, frame = cam.read()
	if (not ret): exit(1)
	
	result, numDetections, boxes = detect(frame)

	annotated_img = result.plot()

	cv2.imshow("output", annotated_img)
	if cv2.waitKey(1) == ord('q'):
		break

