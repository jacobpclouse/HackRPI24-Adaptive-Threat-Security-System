import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import cv2
import numpy as np
import json
from pathlib import Path

me = "rpi.crime.catcher@gmail.com"
with open(Path("passwords.json")) as f:
	password = json.load(f)["gmail"]

def sendEmail(to:str, body:str, image:np.ndarray|None = None):
	msg = MIMEMultipart()
	msg['Subject'] = 'Detected Weapon'
	msg['From'] = me
	msg['To'] = to

	msg.attach(MIMEText(body))

	if image != None:
		_, image_encoded = cv2.imencode('.jpg', image)  # Encode as JPEG format
		msg.attach(MIMEImage(image_encoded.tobytes(), name="gunImage.jpg"))

	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(me, password)
	s.sendmail(me, [to], msg.as_string())
	s.quit()