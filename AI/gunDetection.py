import cv2
from ultralytics import YOLO
from ultralytics.engine.results import Results

# load 
model = YOLO('AI/model.pt', verbose=False)

class Box:
	def __init__(self, x1, y1, x2, y2):
		self.x1 = x1; self.y1 = y1
		self.x2 = x2; self.y2 = y2
		self.x = (x1 + x2)/2
		self.y = (y1 + y2)/2

def detect(img) -> tuple[Results, int, list[Box]] :
	"""
	Pass a image and it will return a tuple of:
	\tThe results object made by YOLO
	\tA int of the number of detected guns
	\tA list of Box classes which contains the gun locations
	"""
	result:Results = model(img, verbose=False)[0]
	boxesNp = result.boxes.xyxy.numpy()
	numDetections = boxesNp.shape[0]
	boxes = []
	for i in range(numDetections):
		box = boxesNp[i]
		boxes.append(Box(box[0], box[1], box[2], box[3]))
	return result, numDetections, boxes
