import cv2
import time
import os
from datetime import datetime
from utils.upload_image import upload_image
from utils.twilio_alert import send_alert_with_image

stop_detection_flag = False
status = "Stopped"

def start_detection():
    global stop_detection_flag, status
    stop_detection_flag = False
    status = "Running"

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        status = "Camera Error"
        return

    print("✅ Camera opened")
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    os.makedirs("recordings/videos", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    log_file = "logs/motion_logs.txt"

    video_writer = None
    is_recording = False
    last_motion_time = 0
    last_alert_time = 0

    RECORD_STOP_DELAY = 5
    ALERT_COOLDOWN = 20

    while not stop_detection_flag:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))

        boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))

        human_detected = False

        for (x, y, w, h) in boxes:
            if w * h < 15000:
                continue
            human_detected = True
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        now = time.time()

        if human_detected:
            status = "Human Detected"
            last_motion_time = now

            if not is_recording:
                filename = f"recordings/videos/human_{int(now)}.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
                is_recording = True

                with open(log_file, "a") as f:
                    f.write(f"[{datetime.now()}] Human detected\n")

            if now - last_alert_time > ALERT_COOLDOWN:
                last_alert_time = now
                img_path = f"recordings/screenshots/human_{int(now)}.jpg"
                cv2.imwrite(img_path, frame)
                image_url = upload_image(img_path)
                send_alert_with_image(image_url)

        if is_recording and (now - last_motion_time) > RECORD_STOP_DELAY:
            video_writer.release()
            video_writer = None
            is_recording = False
            status = "Running"

        if is_recording and video_writer:
            video_writer.write(frame)

        cv2.imshow("Smart Human Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    if video_writer:
        video_writer.release()
    cv2.destroyAllWindows()
    status = "Stopped"


def stop_detection():
    global stop_detection_flag
    stop_detection_flag = True


def get_status():
    return status
