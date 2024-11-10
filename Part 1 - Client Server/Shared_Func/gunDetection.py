from ultralytics import YOLO
from ultralytics.engine.results import Results
from pathlib import Path
import torch

# load 
model = YOLO(Path('Part 1 - Client Server/Models/model.pt'), verbose=False)
# model = YOLO(Path('../Models/model.pt'), verbose=False)
# model = YOLO(Path('Models/model.pt'), verbose=False)
if torch.cuda.is_available():
    model.to('cuda')


class Box:
	def __init__(self, x1, y1, x2, y2):
		self.x1 = int(x1); self.y1 = int(y1)
		self.x2 = int(x2); self.y2 = int(y2)
		self.x = int((x1 + x2)/2)
		self.y = int((y1 + y2)/2)

def detect(img, result:list[tuple[Results, int, list[Box]]]|None = None) -> tuple[Results, int, list[Box]]|None :
	"""
	Pass a image and it will return a tuple of:
	\tThe results object made by YOLO
	\tA int of the number of detected guns
	\tA list of Box classes which contains the gun locations
	If you pass in a list into the second pram it will append the output to the list instead
	"""
	modelResult:Results = model.predict(img, verbose=False, imgsz=640)[0]
	boxesNp = modelResult.boxes.xyxy.cpu().numpy()
	# boxesNp = modelResult.boxes.xyxy.numpy()
	numDetections = boxesNp.shape[0]
	boxes = []
	for i in range(numDetections):
		box = boxesNp[i]
		boxes.append(Box(box[0], box[1], box[2], box[3]))
	if result is None:
		return modelResult, numDetections, boxes
	result.append((modelResult, numDetections, boxes))
