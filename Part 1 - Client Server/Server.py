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

from Shared_Func.utility_functions import (myLogo, defang_datetime, draw_text_on_frame,
                                                createFolderIfNotExists, sanitize_filename,
                                                emptyFolder, clear_screen, eye_animation, get_private_ip)

OUTPUT_FOLDER_NAME = 'CLIENT_VIDEO_STORAGE'
clients = []
frames = {}
frame_count = {}
start_time_dict = {}

DATABASE_NAME = 'CameraInfo.db'
TABLE_NAME = 'VideoMetadata'

createFolderIfNotExists(OUTPUT_FOLDER_NAME)

default_resolutions = ['480x320','640x480', '800x600', '1024x768', '1280x720', '1920x1080']
default_columns = [1, 2, 3, 4]

current_resolution = '480x320'
current_columns = 3

root = ttk.Window(themename="darkly")
root.title("Online Security System - Server")

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

columns_label = ttk.Label(root, text="Select Columns:")
columns_label.pack(pady=5)
columns_dropdown = ttk.Combobox(root, values=default_columns, state="readonly")
columns_dropdown.set(current_columns)
columns_dropdown.pack(pady=5)

def update_settings():
    global current_resolution, current_columns
    current_resolution = resolution_dropdown.get()
    current_columns = int(columns_dropdown.get())
    print(f"Update Setting: current_resolution {current_resolution}, current_columns {current_columns}")

resolution_dropdown.bind("<<ComboboxSelected>>", lambda e: update_settings())
columns_dropdown.bind("<<ComboboxSelected>>", lambda e: update_settings())

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
    global frames, frame_count, start_time_dict
    try:
        print(f"CLIENT {addr} CONNECTED!")
        if client_socket:
            metadata_size = struct.unpack("Q", client_socket.recv(struct.calcsize("Q")))[0]
            metadata_bytes = client_socket.recv(metadata_size)
            client_metadata = pickle.loads(metadata_bytes)

            camera_name = client_metadata["camera_name"]
            location = client_metadata["location"]
            camera_ip = client_metadata["camera_ip"]
            start_time = datetime.now()
            start_time_dict[addr] = start_time
            frame_count[addr] = 0
            
            data = b""
            payload_size = struct.calcsize("Q")
            fourcc = cv2.VideoWriter_fourcc(*'H264')

            out = None
            filename = f'{camera_name}_loc_{location}_time_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4'
            video_filename = os.path.join(OUTPUT_FOLDER_NAME, filename)

            stop_time = None
            metadata_filename = video_filename.replace('.mp4', '.json')

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

                frame_count[addr] += 1
                current_time = datetime.now()
                elapsed_time = (current_time - start_time_dict[addr]).total_seconds()
                fps = frame_count[addr] / elapsed_time if elapsed_time > 0 else 0

                text_top = f"{camera_ip} | {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                frame = draw_text_on_frame(frame, text_top, (10, 30))

                text_bottom = f"FPS: {fps:.2f} | CAM: {camera_name} | BLDG: {location}"
                height, width, _ = frame.shape
                frame = draw_text_on_frame(frame, text_bottom, (10, height - 30))

                frames[addr] = frame

                if out is None:
                    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                out.write(frame)

            if out is not None:
                out.release()

        del frames[addr]
        client_socket.close()

    except Exception as e:
        print(f"CLIENT {addr} DISCONNECTED: {e}")
        frames.clear()
        
        stop_time = datetime.now()

        if addr in start_time_dict:
            metadata = get_metadata(camera_name, camera_ip, location, start_time_dict[addr], stop_time)
            save_metadata(metadata, metadata_filename)
            insert_metadata(camera_name, camera_ip, location, start_time_dict[addr], stop_time, metadata_filename)

# Add this line to create a frame for video displays below the dropdowns
# video_frame = ttk.Frame(root)
# video_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

def update_display():
    global current_resolution, current_columns
    res_width, res_height = map(int, current_resolution.split('x'))
    max_columns = current_columns
    row, col = 0, 0

    # Clear the video_frame content before updating to prevent stacking
    for widget in video_frame.winfo_children():
        widget.destroy()

    for addr in list(frames.keys()):
        frame = frames[addr]
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

def on_start():
    threading.Thread(target=start_server, daemon=True).start()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

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

def change_theme(event):
    new_theme = theme_dropdown.get()
    style.theme_use(new_theme)
    root.update_idletasks()  # Refresh the GUI to apply the new theme

theme_label = ttk.Label(root, text="Select Theme:")
theme_label.pack(pady=5)
theme_dropdown = ttk.Combobox(root, values=style.theme_names(), state="readonly")
theme_dropdown.set('darkly')
theme_dropdown.bind("<<ComboboxSelected>>", change_theme)
theme_dropdown.pack(pady=5)

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