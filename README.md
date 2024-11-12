# Crime Catcher <img src="Part 2 - Dashboard Backend/Frontend_Quasar/frontend-webdashboard/public/eye_white.svg" alt="Crime Catcher" style="height: 1em;"> 
> Safety Through Vigilance!
#### REPO: HackRPI24-Adaptive-Threat-Security-System - Submitted <a href="https://devpost.com/software/crime-catcher">via Devpost</a> to HackRPI 2024 Urban Upgrades
[![GitHub contributors](https://img.shields.io/github/contributors/jacobpclouse/HackRPI24-Adaptive-Threat-Security-System.svg)]("https://github.com/jacobpclouse/HackRPI24-Adaptive-Threat-Security-System/graphs/contributors") <img src="https://img.shields.io/badge/HackRPI%202024-Urban%20Upgrades-red" />
<img src="https://img.shields.io/badge/Technologies-openCV%20Tkinter%20flask%20Quasar%20Vuejs%20sqlite%20yolo%20kaggle-blue" />
<img src="https://img.shields.io/badge/Crime-Catcher-purple.svg?logo=data:image/svg%2bxml;base64,IDxzdmcgIHZlcnNpb249IjEuMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiAgd2lkdGg9IjMwMC4wMDAwMDBwdCIgaGVpZ2h0PSIyMDUuMDAwMDAwcHQiIHZpZXdCb3g9IjAgMCAzMDAuMDAwMDAwIDIwNS4wMDAwMDAiICBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJ4TWlkWU1pZCBtZWV0Ij4gIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAuMDAwMDAwLDIwNS4wMDAwMDApIHNjYWxlKDAuMTAwMDAwLC0wLjEwMDAwMCkiIGZpbGw9IiNmZmZmZmYiIHN0cm9rZT0ibm9uZSI+IDxwYXRoIGQ9Ik0xNDgwIDIwMDYgYzAgLTIgLTI1IC0xMDIgLTU2IC0yMjIgLTgwIC0zMTMgLTgzIC0zMjcgLTg0IC0zNTEgMCAtMjMgMSAtMjMgMTUwIC0yMyAxMjggMCAxNTIgMiAxNTcgMTYgMyA5IC04IDY2IC0yNCAxMjcgLTE3IDYyIC01MCAxOTAgLTczIDI4NSAtMjkgMTE2IC00NyAxNzIgLTU3IDE3MiAtNyAwIC0xMyAtMiAtMTMgLTR6Ii8+IDxwYXRoIGQ9Ik04NTIgMTQ3MyBsMyAtMzE4IDE3OSAtMyBjMTAyIC0xIDE4NCAyIDE4OSA3IDYgNiAtMTggNTYgLTYyIDEzMyAtNDAgNjcgLTEyMCAyMDYgLTE3OSAzMDcgLTU5IDEwMiAtMTEzIDE4NiAtMTIwIDE4OSAtMTAgMyAtMTIgLTYyIC0xMCAtMzE1eiIvPiA8cGF0aCBkPSJNMjA1NCAxNjgyIGMtMTA1IC0xODQgLTI3NSAtNDc2IC0yODYgLTQ4OSAtNiAtNyAtOCAtMjAgLTQgLTI4IDUgLTEzIDMyIC0xNSAxODggLTEzIGwxODMgMyAzIDMxOCBjMiAyNTAgMCAzMTcgLTEwIDMxNyAtNyAwIC00MCAtNDkgLTc0IC0xMDh6Ii8+IDxwYXRoIGQ9Ik0xMjkwIDEwODQgYy0xNzQgLTExMyAtMjg3IC0xNzcgLTUwNyAtMjg3IC0xNTYgLTc4IC0yODMgLTE0NyAtMjgzIC0xNTIgMCAtNiAxMDAgLTYxIDIyMyAtMTIzIDEzMCAtNjYgMjg4IC0xNTUgMzgyIC0yMTcgODggLTU3IDE3MCAtMTEwIDE4MiAtMTE3IDEyIC03IDcwIC00NCAxMjggLTgxIGwxMDYgLTY4IDcyIDQ2IGM0MCAyNSAxNDQgOTMgMjMyIDE1MCAyMDkgMTM2IDI0OCAxNTkgNTA0IDI5MCAxMTkgNjEgMjE2IDExNSAyMTUgMTIwIDAgNiAtMzIgMjYgLTcwIDQ1IC0zMDEgMTUyIC01ODAgMzAwIC02MzkgMzM4IC0zOCAyNSAtMTIzIDgxIC0xODggMTI0IC02NiA0MyAtMTIyIDc4IC0xMjYgNzggLTQgMCAtMTA4IC02NiAtMjMxIC0xNDZ6IG00MjcgLTQwIGMxMDQgLTU0IDIxMSAtMTExIDIzOCAtMTI5IDQ1IC0yOSAxMzMgLTg2IDM1NCAtMjMwIGw3NSAtNDggLTMzIC0yNSBjLTkyIC03MSAtMzA1IC0xOTYgLTU1MSAtMzIyIGwtMjc0IC0xNDIgLTY4IDMzIGMtMzcgMTggLTY4IDM1IC02OCAzOSAwIDMgODggOTMgMTk1IDIwMCAxMDcgMTA3IDE5NSAxOTkgMTk1IDIwNSAwIDUgLTkxIDEwMSAtMjAyIDIxMiBsLTIwMyAyMDMgLTIwNyAtMjA3IC0yMDggLTIwOCAxODggLTE4OSBjMTAzIC0xMDMgMTgzIC0xODcgMTc3IC0xODUgLTU1IDIwIC00MzIgMjIzIC01MDggMjc0IC01NCAzNiAtMTAyIDY1IC0xMDUgNjUgLTQgMSAtMjAgMTEgLTM2IDI0IGwtMjkgMjQgMjQgMTMgYzIzIDEyIDExNCA3MCAzMDkgMTk4IDc1IDQ5IDUyMyAyODkgNTQyIDI5MCA0IDEgOTIgLTQyIDE5NSAtOTV6Ii8+IDxwYXRoIGQ9Ik01MCAxMTQyIGMwIC05IDQgLTEyIDMwMCAtMTY3IDExOCAtNjIgMjM2IC0xMjUgMjYzIC0xMzkgMjYgLTE1IDUyIC0yNCA1NyAtMjEgNiA0IDEwIDc0IDEwIDE3MSBsMCAxNjQgLTMxNSAwIGMtMTczIDAgLTMxNSAtNCAtMzE1IC04eiIvPiA8cGF0aCBkPSJNMjMxMCA5ODcgYzAgLTkwIDMgLTE2NyA3IC0xNzAgMyAtNCA4MSAzMiAxNzIgODAgNDAxIDIwOCA0NDEgMjMxIDQ0MSAyNDQgMCA1IC0xMjYgOSAtMzEwIDkgbC0zMTAgMCAwIC0xNjN6Ii8+IDwvZz4gPC9zdmc+IA=="/>
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

## Technologies Used:
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)
![YOLO](https://img.shields.io/badge/YOLO-00FFFF?style=for-the-badge&logo=yolo&logoColor=black)
![Quasar](https://img.shields.io/badge/Quasar-1976D2?style=for-the-badge&logo=quasar&logoColor=white)

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

