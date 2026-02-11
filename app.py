import os
import threading
from flask import Flask, render_template, send_from_directory, jsonify
import motion_detector
app = Flask(__name__)
VIDEO_FOLDER = "recordings/videos"
detection_thread = None
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start_detection():
    global detection_thread

    if detection_thread is None or not detection_thread.is_alive():
        detection_thread = threading.Thread(
            target=motion_detector.start_detection,
            daemon=True
        )
        detection_thread.start()
        return "Detection started ✅"

    return "Detection already running ⚠"

@app.route('/stop')
def stop_detection():
    motion_detector.stop_detection()
    return "Detection stopped ⏹"

@app.route('/videos')
def list_videos():
    if not os.path.exists(VIDEO_FOLDER):
        return jsonify([])

    files = [
        f for f in os.listdir(VIDEO_FOLDER)
        if f.lower().endswith('.mp4')
    ]
    return jsonify(files)

@app.route('/download/<filename>')
def download_video(filename):
    return send_from_directory(
        VIDEO_FOLDER,
        os.path.basename(filename),
        as_attachment=True
    )

@app.route('/stream/<filename>')
def stream_video(filename):
    return send_from_directory(
        VIDEO_FOLDER,
        filename,
        mimetype='video/avi'
    )
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_video(filename):
    path = os.path.join(VIDEO_FOLDER, os.path.basename(filename))
    if os.path.exists(path):
        os.remove(path)
        return jsonify({"message": "Video deleted"})
    return jsonify({"message": "File not found"}), 404
@app.route('/status')
def get_status():
    if motion_detector.stop_detection_flag:
        return "Stopped"
    else:
        return "Running"


if __name__ == "__main__":
    app.run(debug=True)
    
