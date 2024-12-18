import cv2
from gunDetection import detect, Results, Box
# from detect import detect_motion

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Error: Could not open camera.")
    exit(1)

baseline = None

while True:
    ret, frame = cam.read()
    if (not ret): exit(1)
    out:list[tuple[Results, int, list[Box]]] = []
    detect(frame, out)
    result, numDetections, boxes = out[0]
    
    for box in boxes:
        box.draw(frame)

    cv2.imshow("output", frame)
    
    # md, baseline = detect_motion(frame, baseline)
    # if md:
    #     cv2.rectangle(frame, (5, 5), (frame.shape[1]-5, frame.shape[0]-5), (0, 0, 255), 4)
    # cv2.imshow("output", frame)

    if cv2.waitKey(1) == ord('q'):
        break

