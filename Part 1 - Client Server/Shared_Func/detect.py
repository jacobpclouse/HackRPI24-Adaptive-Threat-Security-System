import cv2
import time
def detect_motion(frame, baseline, threshold=25, min_contour_area=500):
    motion_detected = False

    if baseline is not None:
        # Convert the current frame to grayscale and blur to reduce noise
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Calculate difference between the baseline and current frame
        frame_delta = cv2.absdiff(baseline, gray)
        _, thresh = cv2.threshold(frame_delta, threshold, 255, cv2.THRESH_BINARY)

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < min_contour_area:
                continue  # Ignore small contours

            # Motion detected in large enough area
            motion_detected = True
            break  # Exit after detecting the first significant motion

    # If no baseline, initialize the baseline using the first frame
    baseline_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    baseline_gray = cv2.GaussianBlur(baseline_gray, (21, 21), 0)  # Smooth the baseline
    baseline = baseline_gray

    return motion_detected, baseline
