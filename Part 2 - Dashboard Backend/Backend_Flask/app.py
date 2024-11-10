from Flask_Functions.generalFunctions import sanitize_filename,emptyFolder

from flask import Flask, request, jsonify, send_file, Response,abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from werkzeug.security import safe_join  # Updated import

import subprocess
import os,re
import sqlite3

PREPATH = 'C:\\Users\\clous\\Downloads\\test bOI\\HackRPI24-Adaptive-Threat-Security-System\\Part 1 - Client Server\\'
CAMERA_DATABASE = os.path.join(PREPATH, 'CameraInfo.db')
VIDEO_STORAGE_PATH = os.path.join(PREPATH, 'CLIENT_VIDEO_STORAGE\\')

TABLE_NAME = 'VideoMetadata'

PREFIX_TO_REPLACE = 'CLIENT_VIDEO_STORAGE\\'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Using SQLite for simplicity
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change this to something more secure

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create the database
with app.app_context():
    db.create_all()


def convert_video_to_h264(video_path):
    # Define the path for the converted video
    converted_video_path = video_path.replace('.mp4', '_converted.mp4')
    
    # Run the ffmpeg command to convert the video
    command = [
        'ffmpeg', '-i', video_path, 
        '-c:v', 'libx264', '-c:a', 'aac', 
        converted_video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Check if the conversion was successful
    if result.returncode == 0:
        return converted_video_path
    else:
        print(f"Error converting video: {result.stderr.decode()}")
        return None
    
# User Signup Route
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# User Login Route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

#--
# Sample route for sending data to the frontend
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)
#--


# populate dashboard with videos
@app.route('/api/videos', methods=['GET'])
def get_videos():
    print('HIT API VIDEOS - non blob')
    conn = sqlite3.connect(CAMERA_DATABASE)
    # conn = sqlite3.connect('CameraInfo.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    # cursor.execute("SELECT * FROM VideoMetadata")
    rows = cursor.fetchall()

    print(f"Rows of data: {rows}")

    videos = []
    for row in rows:
        video_filename = row[6]
        video_filename = video_filename.replace(PREFIX_TO_REPLACE, '')
        # video_filename = video_filename.replace('CLIENT_VIDEO_STORAGE\\', '')
        video_path = os.path.join(VIDEO_STORAGE_PATH, video_filename)
        
        if os.path.exists(video_path):
            video = {
                'id': row[0],
                'camera_name': row[1],
                'camera_ip': row[2],
                'location': row[3],
                'start_time': row[4],
                'stop_time': row[5],
                'video_filename': video_filename,
                'video_url':f"http://localhost:5000/videos/{video_filename}"
            }
            videos.append(video)
        else:
            print(f"Video file {video_path} not found")

    conn.close()

    print(f'json data videos: {videos}')
    return jsonify(videos)

# Fetch video details by ID
@app.route('/api/video/<int:video_id>', methods=['GET'])
def get_video(video_id):
    conn = sqlite3.connect(CAMERA_DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?", (video_id,))
    # cursor.execute("SELECT * FROM VideoMetadata WHERE id = ?", (video_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        video_filename = row[6].replace(PREFIX_TO_REPLACE, '')
        video_path = os.path.join(VIDEO_STORAGE_PATH, video_filename)
        return jsonify({
            'id': row[0],
            'camera_name': row[1],
            'camera_ip': row[2],
            'location': row[3],
            'start_time': row[4],
            'stop_time': row[5],
            'video_filename': video_filename,
            'video_url': f"http://localhost:5000/videos/{video_filename}"
        })
    else:
        return jsonify({"message": "Video not found"}), 404


@app.route('/videos/<filename>', methods=['GET'])
def serve_video(filename):
    filename = filename.replace('.json','.mp4')
    video_path = safe_join(VIDEO_STORAGE_PATH, filename)
    app.logger.debug(f"Requested Video Path: {video_path}")

    if os.path.exists(video_path):
        return send_file(video_path, mimetype='video/mp4', as_attachment=False, download_name=filename)
    else:
        return jsonify({"message": "Video not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
