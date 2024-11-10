from ultralytics import YOLO
from ultralytics.engine.results import Results
from pathlib import Path
import cv2
import torch

# load 
model = YOLO(Path('Part 1 - Client Server/Models/model.pt'), verbose=False)
# model = YOLO(Path('../Models/model.pt'), verbose=False)
# model = YOLO(Path('Models/model.pt'), verbose=False)
if torch.cuda.is_available():
    model.to('cuda')

font = cv2.FONT_HERSHEY_SIMPLEX
fontColor = (255,255,255)
boxColor = (255,0,0)
thickness = 4
lineType = cv2.LINE_AA

class Box:
    def __init__(self, x1, y1, x2, y2, conf, name):
        self.x1 = int(x1); self.y1 = int(y1)
        self.x2 = int(x2); self.y2 = int(y2)
        self.x = int((x1 + x2)/2)
        self.y = int((y1 + y2)/2)
        self.conf = float(conf)
        self.name = str(name)

    def draw(self, img):
        fontScale = img.shape[0]/600
        cv2.rectangle(img, (self.x1, self.y1), (self.x2, self.y2), boxColor, 4)
        text = self.name + " " + str(round(self.conf, 2))
        textSize = cv2.getTextSize(text, font, fontScale=fontScale, thickness=1)[0]
        textPos = (self.x1, self.y1)
        cv2.rectangle(img, (textPos[0], textPos[1]-textSize[1]), (textPos[0]+textSize[0], textPos[1]), boxColor, cv2.FILLED)

        cv2.putText(
            img,
            text,
            textPos, 
            font, 
            fontScale,
            fontColor,
            thickness,
            lineType
        )

    def __str__(self):
        return f"(({self.x1}, {self.x1}), ({self.x1}, {self.x1}), conf: {self.conf})"

def detect(img, result:list[tuple[Results, int, list[Box]]]|None = None) -> tuple[Results, int, list[Box]]|None:
    """
    Pass a image and it will return a tuple of:
    \tThe results object made by YOLO
    \tA int of the number of detected guns
    \tA list of Box classes which contains the gun locations
    If you pass in a list into the second pram it will append the output to the list instead
    """
    img = img.copy()
    modelResult:Results = model.predict(img, verbose=False, imgsz=640, conf=0.4)[0]
    boxesNp = modelResult.boxes.xyxy.cpu().numpy()
    boxesConfNp = modelResult.boxes.conf.cpu().numpy()
    boxesClsNp = modelResult.boxes.cls.cpu().numpy()
    names = modelResult.names
    numDetections = boxesNp.shape[0]
    boxes:list[Box] = []
    for i in range(numDetections):
        box = boxesNp[i]
        boxes.append(Box(box[0], box[1], box[2], box[3], boxesConfNp[i], names[int(boxesClsNp[i])]))
        boxes[i].draw(img)
    
    if result is None:
        return img, numDetections, boxes
    result.append((img, numDetections, boxes))
