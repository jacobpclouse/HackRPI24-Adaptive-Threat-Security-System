# dedicated to Darrin Chatman - future Software Developer
import os
import time
import socket
import cv2

# draw text on frame:
def draw_text_on_frame(frame, text, position, font_scale=1.3, color=(255, 255, 255), thickness=3):
# def draw_text_on_frame(frame, text, position, font_scale=0.7, color=(255, 255, 255), thickness=2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
    return frame

#get private ip inside network of the server computer
def get_private_ip():
    try:
        host_name = socket.gethostname()
        print(f"Computer Hostname: {host_name}")

        # Connect to an external server (Google's DNS server in this case)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        private_ip = s.getsockname()[0]
        s.close()
        return private_ip
    except Exception as e:
        return f"Unable to get IP: {e}"

# --- Function to print out my Logo ---
def myLogo():
    
    print("Welcome to your very own:")
    print("   ___     _                    ___      _       _               ")
    print("  / __\ __(_)_ __ ___   ___    / __\__ _| |_ ___| |__   ___ _ __ ")
    print(" / / | '__| | '_ ` _ \ / _ \  / /  / _` | __/ __| '_ \ / _ \ '__|")
    print("/ /__| |  | | | | | | |  __/ / /__| (_| | || (__| | | |  __/ |   ")
    print("\____/_|  |_|_| |_| |_|\___| \____/\__,_|\__\___|_| |_|\___|_|   ")
                                                                 
    print('--- === --- === ------ === --- === ------ === --- === ---  === ---  === --- ')
    print("Safety through Vigilance! Brought to you by Drew, Ben, Dayyan and Jacob")
    print('--- === --- === ------ === --- === ------ === --- === ---  === ---  === --- ')



# --- Function to create a folder if it does not exist ---
def createFolderIfNotExists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def clear_screen():
    # Clears the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

def eye_animation(inputText='LOADING'):
    # got eye template from: https://emojicombos.com/eye-ascii-art
    frames = [
        '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣤⣴⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⠿⠛⠋⠉⠁⠀⠀⠀⠈⠙⠻⢷⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣤⣾⡿⠋⠁⠀⣠⣶⣿⡿⢿⣷⣦⡀⠀⠀⠀⠙⠿⣦⣀⠀⠀⠀⠀
⠀⠀⢀⣴⣿⡿⠋⠀⠀⢀⣼⣿⣿⣿  ⢻⣽⣿⡆⠀⠀⠀⠀⢻⣿⣷⣶⣄⠀
⠀⣴⣿⣿⠋⠀⠀⠀⠀⠸⣿⣿⣿⣿  ⢸⣿⣿⣿⠀⠀⠀⠐⡄⡌⢻⣿⣿⡷
⢸⣿⣿⠃⢂⡋⠄⠀⠀⠀⢿⣿⣿⣿ ⣴⣯⣿⣿⠏⠀⠀⠀⠀⢦⣷⣿⠿⠛⠁
⠀⠙⠿⢾⣤⡈⠙⠂⢤⢀⠀⠙⠿⢿⣿⣿⡿⠟⠁⠀⣀⣀⣤⣶⠟⠋⠁⠀⠀⠀
⠀⠀⠀⠀⠈⠙⠿⣾⣠⣆⣅⣀⣠⣄⣤⣴⣶⣾⣽⢿⠿⠟⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠙⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    
''',  # Center

        '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣤⣴⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⠿⠛⠋⠉⠁⠀⠀⠀⠈⠙⠻⢷⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣤⣾⡿⠋⣠⣶⣿⡿⣿⣷⣦⡀⠁⠀⠀⠀⠀⠙⠿⣦⣀⠀⠀⠀⠀
⠀⠀⢀⣴⣿⡿⠋⢀⣼ ⠙⣿⣿⣾⣽⣿⡆⠀⠀⠀⠀⠀⠀ ⢻⣿⣷⣶⣄⠀
⠀⣴⣿⣿⠋⠀⠀⠸⣿   ⣯⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠐⡄⡌⢻⣿⣿⡷
⢸⣿⣿⠃⢂⡋⠄⢿⣿ ⣠⣿⣿⣯⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⢦⣷⣿⠿⠛⠁
⠀⠙⠿⢾⣤⡈⠙⠂⢤⠙⠿⢿⣿⣿⡿⠟⠁⢀⠀⠀⣀⣀⣤⣶⠟⠋⠁⠀⠀⠀
⠀⠀⠀⠀⠈⠙⠿⣾⣠⣆⣅⣀⣠⣄⣤⣴⣶⣾⣽⢿⠿⠟⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠙⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀             
''',  # Left

        '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣤⣴⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⠿⠛⠋⠉⠁⠀⠀⠀⠈⠙⠻⢷⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣤⣾⡿⠋⠁⠀⠀⠀⠀⣠⣶⣿⢿⡿⣷⣦⡀⠙⠿⣦⣀⠀⠀⠀⠀
⠀⠀⢀⣴⣿⡿⠋⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣽⣾⠋ ⣿⡆⠀⢻⣿⣷⣶⣄⠀
⠀⣴⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿   ⣿⠐⡄⡌⢻⣿⣿⡷
⢸⣿⣿⠃⢂⡋⠄⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣦ ⣿⠏⠀⢦⣷⣿⠿⠛⠁
⠀⠙⠿⢾⣤⡈⠙⠂⢤⢀⠀⠀⣀⠙⠿⢿⣿⣿⡿⠟⠁⣀⣤⣶⠟⠋⠁⠀⠀⠀
⠀⠀⠀⠀⠈⠙⠿⣾⣠⣆⣅⣀⣠⣄⣤⣴⣶⣾⣽⢿⠿⠟⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠙⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  
'''
    ]

    start_time = time.time()
    while time.time() - start_time < 2:
        for frame in frames:
            clear_screen()
            print("Crime Catcher: Safety through Vigilance!\n")
            print(frame)
            time.sleep(0.2)

    # After the animation, clear the screen and show "LOADING"
    clear_screen()
    print(inputText)
    # print("--- === --- START SERVER LOG --- === ---")
