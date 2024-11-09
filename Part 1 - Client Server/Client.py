import socket
import pickle
import struct
import threading
import cv2
import os
import pyshine as ps
from PIL import Image, ImageTk
import imutils
import tkinter as tk
from tkinter import filedialog, messagebox
from ttkbootstrap import Style
from ttkbootstrap import ttk
from pathlib import Path # for ico

from Shared_Func.utility_functions import (myLogo, defang_datetime, draw_text_on_frame,
                                                createFolderIfNotExists, sanitize_filename,
                                                emptyFolder, clear_screen, eye_animation, get_private_ip)

# Get available webcams
def get_available_webcams():
    print('--- === --- === ------ === --- === ------ === --- === ---  === ---  === --- ')
    print('> HEY! You may see some error messages, this because open cv is looking to see what cameras are available')
    print('--- === --- === ------ === --- === ------ === --- === ---  === ---  === --- ')
    
    webcams = []
    for i in range(10):  # Check the first 10 indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            webcams.append(i)
            cap.release()  # Release the camera
    print('--- === --- === ------ === --- === ------ === --- === ---  === ---  === --- ')
    print('> OK! Should be done with the error messages!')
    print('--- === --- === ------ === --- === ------ === --- === ---  === ---  === --- ')
    print(f'>>> WEBCAMS Available: {webcams} <<<')
    return webcams


def returnIPandPort():
    ip = ip_entry.get()
    port = int(port_entry.get())
    location = location_entry.get()  # Get the location from the new entry
    return ip, port, location  # Return location as well

def send_metadata(client_socket, camera_name, camera_ip, location):
    metadata = {
        "camera_name": camera_name,
        "camera_ip": camera_ip,
        "location": location
    }
    metadata_bytes = pickle.dumps(metadata)
    client_socket.sendall(struct.pack("Q", len(metadata_bytes)) + metadata_bytes)

def start_client():
    ip, port, location = returnIPandPort()  # Get location here
    if not location:  # Check if location is provided
        messagebox.showerror("Input Error", "Building location is mandatory.")
        return
    
    incomingTestVideo = video_path if video_var.get() == 'Video' else None
    vid = None
    camera = False

    # If webcam is selected
    if incomingTestVideo is None:
        camera = True
        selected_webcam_value = webcam_dropdown.get()  # Get the selected webcam value
        selected_webcam_split = int(selected_webcam_value.split(' ')[-1])  # Extract the index from the value
        vid = cv2.VideoCapture(selected_webcam_split)
    else:
        vid = cv2.VideoCapture(incomingTestVideo)

    # Set up client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Attempt to connect to the server with reconnection logic
    for attempt in range(5):
        try:
            client_socket.connect((ip, port))
            break  # Exit loop if connection is successful
        except Exception:
            reconnect_label.config(text=f"RECONNECTING, attempt number {attempt + 1}")
            root.update()  # Update the Tkinter window
            threading.Event().wait(1)  # Wait for 1 second before retrying
    else:
        messagebox.showerror("Connection Error", "Failed to connect to the server after 5 attempts.")
        return

    # Send metadata to server
    if incomingTestVideo is None:
        send_metadata(client_socket, selected_webcam_value, get_private_ip(), location)  # Use the location from user input
    else:
        send_metadata(client_socket, socket.gethostname(), get_private_ip(), "VIDEO-STREAM")

    def stream_video():
        while vid.isOpened():
            try:
                img, frame = vid.read()
                if frame is None:
                    break
                frame = imutils.resize(frame, width=720)
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)

                # Draw a red outline around the frame -- TO SHOW WHEN RECORDING!
                cv2.rectangle(frame, (5, 5), (715, 515), (0, 0, 250), 4)

                # Display the frame in the Tkinter window
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_tk = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
                video_label.config(image=img_tk)
                video_label.image = img_tk  # Keep a reference to avoid garbage collection

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
            except Exception as e:
                print(f"Error while streaming: {e}")
                break
        client_socket.close()

    # Disable IP, port, and video/webcam choice after starting
    ip_entry.config(state=tk.DISABLED)
    port_entry.config(state=tk.DISABLED)
    webcam_dropdown.config(state=tk.DISABLED)
    video_button.config(state=tk.DISABLED)
    video_option_menu.config(state=tk.DISABLED)
    location_entry.config(state=tk.DISABLED)  # Disable location entry as well

    # Start video streaming in a separate thread
    threading.Thread(target=stream_video, daemon=True).start()

def preview_video(selected_webcam_index):
    """Function to display a preview of the selected webcam for 20 seconds."""
    preview_vid = cv2.VideoCapture(selected_webcam_index)

    def show_preview():
        for _ in range(20):  # Show preview for 20 seconds
            ret, frame = preview_vid.read()
            if not ret:
                break

            text_top = "PREVIEW"
            frame = draw_text_on_frame(frame, text_top, (10, 30))

            # Display the frame in the Tkinter window
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_tk = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
            video_label.config(image=img_tk)
            video_label.image = img_tk  # Keep a reference to avoid garbage collection

            cv2.waitKey(50)  # Display each frame for a short time

        preview_vid.release()

    # Start the preview in a separate thread
    threading.Thread(target=show_preview, daemon=True).start()

def start_preview():
    selected_webcam_value = webcam_dropdown.get()  # Get the selected webcam value
    selected_webcam_split = int(selected_webcam_value.split(' ')[-1])  # Extract the index from the value
    preview_video(selected_webcam_split)

def stop_client():
    print('Stopping client...')
    messagebox.showinfo("Client Status", "Client has stopped streaming.")
    root.quit()

def validate_ip_port():
    """Validates IP and port input."""
    ip = ip_entry.get()
    port = port_entry.get()

    try:
        socket.inet_aton(ip)  # Check if IP is valid
        if not (1024 <= int(port) <= 65535):  # Check port range
            raise ValueError
    except Exception:
        start_button.config(state=tk.DISABLED)
        return
    start_button.config(state=tk.NORMAL)

def choose_video():
    global video_path
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    if video_path:
        video_button.config(text="Video selected")

def toggle_webcam_video_options(*args):
    if video_var.get() == "Webcam":
        webcam_dropdown.config(state=tk.NORMAL)
        video_button.config(state=tk.DISABLED)
        preview_button.config(state=tk.NORMAL)  # Enable preview button
    else:
        webcam_dropdown.config(state=tk.DISABLED)
        video_button.config(state=tk.NORMAL)
        preview_button.config(state=tk.DISABLED)  # Disable preview button



# Initialize `ttkbootstrap` styling
# style = Style("cosmo")  # You can choose other themes like "darkly", "superhero", "flatly"
style = Style('darkly')  # You can set your initial theme here

# Root window with `ttkbootstrap` style
root = style.master
root.title("Crime Catcher - Client Stream")

# Set the icon for the window
icon_path = Path(os.path.join("Shared_Func","eye.ico"))  # where ico is, should work on any system
if icon_path.exists():
    root.iconbitmap(icon_path)  # For .ico files
else:
    print(f"Icon file not found at {icon_path}")

# Display client's private IP
private_ip_label = ttk.Label(root, text=f"Private IP: {get_private_ip()}")
private_ip_label.pack()

def change_theme(event):
    new_theme = theme_dropdown.get()
    style.theme_use(new_theme)
    root.update_idletasks()  # Refresh the GUI to apply the new theme

theme_label = ttk.Label(root, text="Select Theme:")
theme_label.pack(pady=5)
theme_dropdown = ttk.Combobox(root, values=style.theme_names(), state="readonly")
# theme_dropdown.set('cosmo')
theme_dropdown.set('darkly')
theme_dropdown.bind("<<ComboboxSelected>>", change_theme)
theme_dropdown.pack(pady=5)


# Reconnection label
reconnect_label = ttk.Label(root, text="")
reconnect_label.pack()

# Start and Stop buttons with `ttkbootstrap`
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

start_button = ttk.Button(button_frame, text="START CLIENT", command=start_client, state=tk.DISABLED, style="success.TButton")
start_button.pack(side=tk.LEFT, padx=5)

stop_button = ttk.Button(button_frame, text="STOP CLIENT", command=stop_client, style="danger.TButton")
stop_button.pack(side=tk.LEFT, padx=5)

# Input for IP, Port, and Location with `ttkbootstrap`
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

# New Location Entry with `ttkbootstrap`
location_label = ttk.Label(ip_port_frame, text="Building Location:")
location_label.grid(row=2, column=0, padx=5, pady=5)
location_entry = ttk.Entry(ip_port_frame)
location_entry.grid(row=2, column=1, padx=5, pady=5)

# Validate IP and port input as user types
ip_entry.bind("<KeyRelease>", lambda event: validate_ip_port())
port_entry.bind("<KeyRelease>", lambda event: validate_ip_port())

# Webcam or Video Selection with `ttkbootstrap`
video_var = tk.StringVar(value="Webcam")
video_option_menu = tk.OptionMenu(root, video_var, "Webcam", "Video", command=toggle_webcam_video_options)
video_option_menu.pack(pady=5)

# Webcam Selection Dropdown with `ttkbootstrap`
webcam_frame = ttk.Frame(root)
webcam_frame.pack(pady=5)
webcam_label = ttk.Label(webcam_frame, text="Select Webcam:")
webcam_label.grid(row=0, column=0, padx=5, pady=5)

# List of available webcams
save_these = get_available_webcams()
webcam_list = [f"Webcam {i}" for i in save_these]
webcam_dropdown = ttk.Combobox(webcam_frame, values=webcam_list, state="readonly")
webcam_dropdown.grid(row=0, column=1, padx=5, pady=5)
webcam_dropdown.current(0)

# Preview Button with `ttkbootstrap`
preview_button = ttk.Button(webcam_frame, text="Preview", command=start_preview, style="primary.TButton")
preview_button.grid(row=0, column=2, padx=5, pady=5)

# Video File Selection Button with `ttkbootstrap`
video_button = ttk.Button(root, text="Choose Video", command=choose_video, state=tk.DISABLED, style="info.TButton")
video_button.pack(pady=5)

# Video display frame
video_frame = ttk.Frame(root)
video_frame.pack()

video_label = ttk.Label(video_frame)
video_label.pack()

# Start the Tkinter event loop
root.mainloop()