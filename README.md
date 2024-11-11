# CRIME CATCHER
> Safety Through Vigilance!
#### REPO: HackRPI24-Adaptive-Threat-Security-System - Submitted to HackRPI 2024 Urban Upgrades
[![GitHub contributors](https://img.shields.io/github/contributors/jacobpclouse/HackRPI24-Adaptive-Threat-Security-System.svg)]("https://github.com/jacobpclouse/HackRPI24-Adaptive-Threat-Security-System/graphs/contributors") <img src="https://img.shields.io/badge/HackRPI%202024-Urban%20Upgrades-red" />
<img src="https://img.shields.io/badge/Technologies-openCV%20Tkinter%20flask%20Quasar%20Vuejs%20sqlite%20yolo%20kaggle-blue" />
## What it does
Crime Catcher is a solution to keeping our urban spaces safe and secure.

It is an online surveillance system where a central server receives camera feeds from remote clients and uses AI to determine if weapons or dangerous objects are in frame. The model is GPU-accelerated for efficient processing.

If a dangerous object is detected, the backend automatically sends an email alert to a trusted contact, ensuring every second counts.

Additionally, we save and catalog videos and metadata using an SQLite database. This data can be browsed for review and analysis after the fact.

### Other Features:

- Clients will automatically try to reconnect if they get disconnected from the server (they will disconnect after 5 attempts).
- We integrate time stamps into the video streams such as frame rate, source IP, source building, etc.
- Users can specify an email address in the server to receive alerts about dangerous objects and weapons.
- We used ttk bootstrap to create beautiful interfaces on both the client and server in part 1.
- For Part 2 (the vue.js/quasar and flask dashboard) we have a login system that enforces users to login before they can access the video metadata, ensuring the system is attributable
- We have motion detection in our server stream so only eventful data is saved to disk, conserving bandwidth

## Challenges we ran into
- Working with Tkinter's documentation and using the CUDA framework in our server for GPU acceleration

## Accomplishments that we're proud of
- Motion detection: Creating logic that pauses recording on the server if there is no motion going on in the camera frame.
- AI weapon detection: Utilizing machine learning to detect and locate weapons.
- Video feed centralization: Gathering multiple camera feeds to effectively track and stop bad actors.

## What we learned
Tkinter documentation is difficult to understand, and we learned how to integrate an AI model into our Tkinter server and how to best select a pre trained model to suite our needs. We also learned more about YOLO and model training.

## What's next for Crime Catcher
After our MVP, we want to iterate and add new features like remote client activation in the next sprint.


## Sources:
- Text on Video with OpenCV: https://www.geeksforgeeks.org/python-opencv-write-text-on-video/
- Ascii art generated using: http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
- Guns detection model from: https://www.kaggle.com/code/ahmedgaitani/guns-object-detection-code
