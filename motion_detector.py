import cv2
import time
import os
from datetime import datetime
from utils.upload_image import upload_image
from utils.twilio_alert import send_alert_with_image
stop_detection_flag = False
def start_detection():
    global stop_detection_flag
    stop_detection_flag = False

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Camera not accessible")
        return

    print("Camera opened")

    back_sub = cv2.createBackgroundSubtractorMOG2(
        history=700,
        varThreshold=80,
        detectShadows=False
    )

    os.makedirs("recordings/videos", exist_ok=True)
    os.makedirs("recordings/screenshots", exist_ok=True)

    WIDTH, HEIGHT = 640, 480
    FPS = 20.0

    video_writer = None
    is_recording = False

    last_motion_time = 0
    last_alert_time = 0
    motion_frame_count = 0

    MIN_CONTOUR_AREA = 10000        
    MIN_MOTION_FRAMES = 5           
    RECORD_STOP_DELAY = 5          
    ALERT_COOLDOWN = 30             

    while not stop_detection_flag:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (WIDTH, HEIGHT))

        fg_mask = back_sub.apply(frame)
        _, fg_mask = cv2.threshold(fg_mask, 250, 255, cv2.THRESH_BINARY)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.dilate(fg_mask, kernel, iterations=2)

        contours, _ = cv2.findContours(
            fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        motion_detected = False

        for cnt in contours:
            if cv2.contourArea(cnt) < MIN_CONTOUR_AREA:
                continue
            motion_detected = True
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        now = time.time()

        if motion_detected:
            motion_frame_count += 1
        else:
            motion_frame_count = 0

        if motion_frame_count >= MIN_MOTION_FRAMES:
            last_motion_time = now

            if not is_recording:
                filename = f"recordings/videos/motion_{int(now)}.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_writer = cv2.VideoWriter(
                    filename, fourcc, FPS, (WIDTH, HEIGHT)
                )
                is_recording = True
                print(" Recording started")

            if now - last_alert_time > ALERT_COOLDOWN:
                last_alert_time = now
                img_path = f"recordings/screenshots/motion_{int(now)}.jpg"
                cv2.imwrite(img_path, frame)

                image_url = upload_image(img_path)
                send_alert_with_image(image_url)
                print("🚨 Alert sent")


        if is_recording and (now - last_motion_time) > RECORD_STOP_DELAY:
            video_writer.release()
            video_writer = None
            is_recording = False
            print("⏹ Recording stopped")

        cv2.putText(
            frame,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        if is_recording and video_writer:
            video_writer.write(frame)

        cv2.imshow("Smart Motion Detection", frame)
        cv2.waitKey(1)

    cap.release()
    if video_writer:
        video_writer.release()
    cv2.destroyAllWindows()
    print(" Detection stopped")


def stop_detection():
    global stop_detection_flag
    stop_detection_flag = True
