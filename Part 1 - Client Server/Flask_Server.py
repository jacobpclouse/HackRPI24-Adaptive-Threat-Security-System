import socket
import pickle
import struct
import threading
import cv2
import os
import json
from datetime import datetime
import sqlite3
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
import tkinter as tk
import tkinter.messagebox as messagebox
from pathlib import Path
from flask import Flask, Response, jsonify
from flask_cors import CORS

from Shared_Func.emailer import sendEmail
from Shared_Func.gunDetection import detect
#added by dayyan 
from Shared_Func.detect import detect_motion  
# from Client import detect_motion


from Shared_Func.utility_functions import (myLogo,draw_text_on_frame,
                                                createFolderIfNotExists,
                                                eye_animation, get_private_ip)



ALERT_EMAIL = "sagejpc5@gmail.com"
# ALERT_EMAIL = "benherman345@gmail.com"
DO_ALERT_EMAIL = False


OUTPUT_FOLDER_NAME = 'CLIENT_VIDEO_STORAGE'
clients = []
frames = {}
frame_count = {}

DATABASE_NAME = 'CameraInfo.db'
TABLE_NAME = 'VideoMetadata'

FLASK_URL = "0.0.0.0"
FLASK_PORT = 5000
# (host="0.0.0.0", port=5000)

createFolderIfNotExists(OUTPUT_FOLDER_NAME)

default_resolutions = ['480','640', '800', '1024', '1280', '1920']
default_columns = [1, 2, 3, 4]

current_resolution = '480'
current_columns = 3

# Initialize Tkinter window
root = ttk.Window(themename="darkly")
root.title("Crime Catcher - Server")

app = Flask(__name__)  # Initialize Flask app for API
CORS(app)  # This will enable CORS for all routes

icon_path = Path(os.path.join("Shared_Func","eye.ico"))
if icon_path.exists():
    root.iconbitmap(icon_path)
else:
    print(f"Icon file not found at {icon_path}")
root.geometry("800x600")


private_ip_label = ttk.Label(root, text=f"Private IP: {get_private_ip()}")
private_ip_label.pack()

resolution_label = ttk.Label(root, text="Select Resolution:")
resolution_label.pack(pady=5)
resolution_dropdown = ttk.Combobox(root, values=default_resolutions, state="readonly")
resolution_dropdown.set(current_resolution)
resolution_dropdown.pack(pady=5)

# columns_label = ttk.Label(root, text="Select Columns:")
# columns_label.pack(pady=5)
# columns_dropdown = ttk.Combobox(root, values=default_columns, state="readonly")
# columns_dropdown.set(current_columns)
# columns_dropdown.pack(pady=5)

def update_settings():
    global current_resolution, current_columns
    current_resolution = resolution_dropdown.get()
    # current_columns = int(columns_dropdown.get())
    # print(f"Update Setting: current_resolution {current_resolution}, current_columns {current_columns}")
    print(f"Update Setting: current_resolution {current_resolution}")

resolution_dropdown.bind("<<ComboboxSelected>>", lambda e: update_settings())
# columns_dropdown.bind("<<ComboboxSelected>>", lambda e: update_settings())

def setup_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camera_name TEXT,
            camera_ip TEXT,
            location TEXT,
            start_time TEXT,
            stop_time TEXT,
            metadata_filename TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_metadata(camera_name, camera_ip, location, start_time, stop_time, metadata_filename):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''
        INSERT INTO {TABLE_NAME} (camera_name, camera_ip, location, start_time, stop_time, metadata_filename)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (camera_name, camera_ip, location, start_time.strftime("%Y-%m-%d %H:%M:%S"),
          stop_time.strftime("%Y-%m-%d %H:%M:%S"), metadata_filename))
    conn.commit()
    conn.close()

def get_metadata(camera_name, camera_ip, location, start_time, stop_time):
    metadata = {
        "camera_name": camera_name,
        "camera_ip": camera_ip,
        "location": location,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "stop_time": stop_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return metadata

def save_metadata(metadata, filename):
    with open(filename, 'w') as f:
        json.dump(metadata, f, indent=4)

def show_client(addr, client_socket):
    global frames, frame_count
    try:
        cap = cv2.VideoCapture(0)
        print(f"CLIENT {addr} CONNECTED!")
        recording = False
        if client_socket:
            metadata_size = struct.unpack("Q", client_socket.recv(struct.calcsize("Q")))[0]
            metadata_bytes = client_socket.recv(metadata_size)
            client_metadata = pickle.loads(metadata_bytes)

            camera_name = client_metadata["camera_name"]
            location = client_metadata["location"]
            camera_ip = client_metadata["camera_ip"]
            true_start_time = datetime.now()
            start_time = datetime.now()
            frame_count[addr] = 0

            data = b""  # Buffer for receiving frame data
            payload_size = struct.calcsize("Q")
            out = None # VideoWriter object

            # Initialize baseline for motion detection
            baseline = None  
            # Initialize variables for recording state

            fourcc = cv2.VideoWriter_fourcc(*'H264')

            video_recording_stop_time = datetime.now()

            time_of_last_email = datetime.now()

            time_of_last_detection = datetime.now()

            image_processing_boxs = []
            image_processing_thread_result = None
            image_processing_thread = None
            
            # Stream processing loop
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4 * 1024)
                    if not packet:
                        break
                    data += packet
                if not data:
                    break
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += client_socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)

                #resize to allow for higher resilution text
                (h, w) = frame.shape[:2]
                new_width = 1600
                aspect_ratio = h / w
                new_height = int(new_width * aspect_ratio)
                frame = cv2.resize(frame, (new_width, new_height))

                # Detect motion and handle recording
                motion_detected, baseline = detect_motion(frame, baseline, 5)
                if motion_detected:
                    video_recording_stop_time = datetime.now()
                    if not recording:
                        # Start recording if motion is detected
                        start_time = datetime.now()
                        filename = f'{camera_name}_loc_{location}_time_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4'
                        video_filename = os.path.join(OUTPUT_FOLDER_NAME, filename)
                        metadata_filename = video_filename.replace('.mp4', '.json')
                        out = cv2.VideoWriter(video_filename, fourcc, 30.0, (frame.shape[1], frame.shape[0]))
                        recording = True
                        print("Recording started...")
                elif recording and (datetime.now() - video_recording_stop_time).total_seconds() > 10:
                    # Stop recording if no motion detected
                    out.release()
                    out = None
                    recording = False
                    print("Recording stopped.")
                    stop_time = datetime.now()
                    metadata = get_metadata(camera_name, camera_ip, location, start_time, stop_time)
                    save_metadata(metadata, metadata_filename)
                    insert_metadata(camera_name, camera_ip, location, start_time, stop_time, metadata_filename)

                # Always add overlay text to the frame
                frame_count[addr] += 1
                current_time = datetime.now()
                elapsed_time = (current_time - true_start_time).total_seconds()
                fps = frame_count[addr] / elapsed_time if elapsed_time > 0 else 0

                # Add top and bottom overlay text
                text_top = f"{camera_ip} | {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                frame = draw_text_on_frame(frame, text_top, (10, 40))

                text_bottom = f"FPS: {fps:.2f} | CAM: {camera_name} | BLDG: {location} | LD: {(datetime.now() - time_of_last_detection).total_seconds():.2f}"
                height, width, _ = frame.shape
                frame = draw_text_on_frame(frame, text_bottom, (10, height - 30))

                # Write the frame to the video file if recording
                if recording:
                    # pass frame into model here
                    if image_processing_thread is not None and not image_processing_thread.is_alive():
                        image, numDetections, boxes = image_processing_thread_result[0]
                        image_processing_thread = None
                        image_processing_boxs = boxes
                        if DO_ALERT_EMAIL and numDetections > 0 and (datetime.now() - time_of_last_email).total_seconds() > 5:
                            time_of_last_email = datetime.now()
                            threading.Thread(target=sendEmail, args=(ALERT_EMAIL, "Detected Weapon", text_bottom, image)).start()
                    for box in image_processing_boxs:
                        box.draw(frame)

                    if image_processing_thread == None:
                        image_processing_thread_result = []
                        image_processing_thread = threading.Thread(target=detect, args=(frame, image_processing_thread_result))
                        time_of_last_detection = datetime.now()
                        image_processing_thread.start()

                    # end detect
                    out.write(frame)

                # Store the frame for UI display
                frames[addr] = frame

            # Cleanup after the loop
            if recording:
                out.release()
                # save metaData
                stop_time = datetime.now()
                metadata = get_metadata(camera_name, camera_ip, location, start_time, stop_time)
                save_metadata(metadata, metadata_filename)
                insert_metadata(camera_name, camera_ip, location, start_time, stop_time, metadata_filename)

        if addr in frames:
            del frames[addr]
        client_socket.close()

    except Exception as e:
        print(f"CLIENT {addr} DISCONNECTED: {e}")

        # Cleanup
        if addr in frames:
            del frames[addr]
        if recording:
            # close video
            out.release()
            # save metaData
            stop_time = datetime.now()
            metadata = get_metadata(camera_name, camera_ip, location, start_time, stop_time)
            save_metadata(metadata, metadata_filename)
            insert_metadata(camera_name, camera_ip, location, start_time, stop_time, metadata_filename)
        
        try:
            client_socket.close()
        except:
            pass

def update_display():
    global current_resolution, current_columns
    res_width = int(current_resolution)
    
    max_columns = current_columns
    row, col = 0, 0

    # Clear the video_frame content before updating to prevent stacking
    for widget in video_frame.winfo_children():
        widget.destroy()

    for addr in list(frames.keys()):
        try:
            frame = frames[addr]
            (h, w) = frame.shape[:2]
            aspect_ratio = h / w
            res_height = int(res_width * aspect_ratio)
            frame_resized = cv2.resize(frame, (res_width, res_height))
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(image)

            label = ttk.Label(video_frame, image=photo)
            label.image = photo
            label.grid(row=row, column=col, padx=5, pady=5)

            col += 1
            if col >= max_columns:
                col = 0
                row += 1
        except Exception as e:
            print("uh oh we hit the exception in update display!:")
            print(e)

    validate_ip_port()

    # Update every 33 milliseconds
    video_frame.after(33, update_display)

def start_server():
    setup_database()
    eye_animation("--- === --- START SERVER LOG --- === ---")
    myLogo()
    ip = ip_entry.get()
    port = int(port_entry.get())

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen()

    ip_entry.config(state=tk.DISABLED)
    port_entry.config(state=tk.DISABLED)

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=show_client, args=(addr, client_socket))
        client_thread.daemon = True
        clients.append(client_thread)
        client_thread.start()

def validate_ip_port():
    ip = ip_entry.get()
    port = port_entry.get()
    try:
        socket.inet_aton(ip)
        if not (1024 <= int(port) <= 65535):
            raise ValueError
    except Exception:
        start_button.config(state=tk.DISABLED)
        return
    start_button.config(state=tk.NORMAL)

def stream_generator(addr):
    """Generate video frames for Flask streaming."""
    while True:
        if addr in frames:
            frame = frames[addr]
            _, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
        else:
            break


# @app.route('/stream/0')
# def stream_video():
#     return Response(open("path_to_video.mp4", "rb"), mimetype="video/mp4")


@app.route('/stream/<int:client_id>')
def video_feed(client_id):
    """Flask route to stream video of a particular client by ID."""
    if client_id < len(clients):
        addr = list(frames.keys())[client_id]
        return Response(stream_generator(addr),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    return "Client stream not available", 404


def start_flask_server():
    app.run(host=FLASK_URL, port=FLASK_PORT)
    # app.run(host="0.0.0.0", port=5000) # OLD DEFAULT

def on_start():
    threading.Thread(target=start_server, daemon=True).start()
    threading.Thread(target=start_flask_server, daemon=True).start()  # Start Flask server in background
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

# def on_start():
#     threading.Thread(target=start_server, daemon=True).start()
#     start_button.config(state=tk.DISABLED)
#     stop_button.config(state=tk.NORMAL)

def on_stop():
    for client in clients:
        client.join()
    print('Stopping Server...')
    # ttk.messagebox.showinfo("TKK Server Status", "Server has been stopped.")
    messagebox.showinfo("Server Status", "Server has been stopped.")
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)



# Initialize ttkbootstrap style
style = Style('darkly')  # You can set your initial theme here

# def change_theme(event):
#     new_theme = theme_dropdown.get()
#     style.theme_use(new_theme)
#     root.update_idletasks()  # Refresh the GUI to apply the new theme

# theme_label = ttk.Label(root, text="Select Theme:")
# theme_label.pack(pady=5)
# theme_dropdown = ttk.Combobox(root, values=style.theme_names(), state="readonly")
# theme_dropdown.set('darkly')
# theme_dropdown.bind("<<ComboboxSelected>>", change_theme)
# theme_dropdown.pack(pady=5)


# -------
# Add a label and entry for the alert email
email_label = ttk.Label(root, text="Enter Alert Email Address:")
email_label.pack(pady=5)
email_entry = ttk.Entry(root, width=30)
email_entry.insert(0, ALERT_EMAIL)  # Set default email in the entry box
email_entry.pack(pady=5)

def update_alert_email():
    global ALERT_EMAIL
    ALERT_EMAIL = email_entry.get()
    print(f"Updated ALERT_EMAIL: {ALERT_EMAIL}")

# Create a frame to hold the Update Email and Toggle Alert buttons side by side
email_button_frame = ttk.Frame(root)
email_button_frame.pack(pady=5)

# Add a button to update the email
update_email_button = ttk.Button(email_button_frame, text="Update Email", command=update_alert_email)
update_email_button.pack(side=LEFT, padx=5)

# Define the toggle function for the alert email
def toggle_alert_email():
    global DO_ALERT_EMAIL
    DO_ALERT_EMAIL = not DO_ALERT_EMAIL  # Toggle the boolean
    # Update button text
    alert_toggle_button.config(text=f"Alert is {'On' if DO_ALERT_EMAIL else 'Off'}")
    # Update button style based on the state
    if DO_ALERT_EMAIL:
        alert_toggle_button.config(style="danger.TButton")  # Red color
    else:
        alert_toggle_button.config(style="primary.TButton")  # Blue color
    print(f"DO_ALERT_EMAIL set to {DO_ALERT_EMAIL}")

# Add the Toggle Alert Button next to the Update Email button
alert_toggle_button = ttk.Button(
    email_button_frame,
    text=f"Alert is {'On' if DO_ALERT_EMAIL else 'Off'}",
    command=toggle_alert_email,
    style="primary.TButton"  # Initial style based on DO_ALERT_EMAIL being False
)
alert_toggle_button.pack(side=LEFT, padx=5)
# -------

# Start and Stop buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

start_button = ttk.Button(button_frame, text="START SERVER", command=on_start, state=DISABLED)
start_button.pack(side=LEFT, padx=5)

stop_button = ttk.Button(button_frame, text="STOP SERVER", command=on_stop, state=DISABLED)
stop_button.pack(side=LEFT, padx=5)

# IP and Port input
ip_port_frame = ttk.Frame(root)
ip_port_frame.pack(pady=5)

ip_label = ttk.Label(ip_port_frame, text="Server IP:")
ip_label.grid(row=0, column=0, padx=5, pady=5)
ip_entry = ttk.Entry(ip_port_frame)
ip_entry.insert(0, "127.0.0.1")
ip_entry.grid(row=0, column=1, padx=5, pady=5)

port_label = ttk.Label(ip_port_frame, text="Server Port:")
port_label.grid(row=1, column=0, padx=5, pady=5)
port_entry = ttk.Entry(ip_port_frame)
port_entry.insert(0, "9999")
port_entry.grid(row=1, column=1, padx=5, pady=5)

ip_entry.bind("<KeyRelease>", lambda _: validate_ip_port())
port_entry.bind("<KeyRelease>", lambda _: validate_ip_port())

# Video frame
video_frame = ttk.Frame(root)
video_frame.pack(pady=10)

client_labels = {}

# Start updating display
update_display()

root.mainloop()