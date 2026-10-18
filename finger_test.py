
import cv2
import mediapipe as mp
import time
from pathlib import Path
import math

model_path = str(Path(__file__).with_name("hand_landmarker.task"))

BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = mp.tasks.vision.HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

def calculate_angle(a, b, c):
    angle1 = math.atan2(a.y - b.y, a.x - b.x)
    angle2 = math.atan2(c.y - b.y, c.x - b.x)
    angle = abs(math.degrees(angle1 - angle2))

    if angle > 180:
        angle = 360 - angle

    return angle

with mp.tasks.vision.HandLandmarker.create_from_options(options) as landmarker:
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open webcam.")
    else:
        print("Show your hand. Press Q to quit.")

        while True:
            success, frame = camera.read()

            if not success:
                print("Could not read webcam frame.")
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb
            )

            timestamp = int(time.monotonic() * 1000)
            result = landmarker.detect_for_video(image, timestamp)

            fingers = [0, 0, 0, 0, 0]

            if result.hand_landmarks:
                landmarks = result.hand_landmarks[0]

                # Thumb
                thumb_angle = calculate_angle(
                    landmarks[2], landmarks[3], landmarks[4]
                )
                if thumb_angle > 150:
                    fingers[0] = 1

                # Index, middle, ring and little fingers
                finger_points = [
                    (5, 6, 8),
                    (9, 10, 12),
                    (13, 14, 16),
                    (17, 18, 20)
                ]

                for i, (base, joint, tip) in enumerate(finger_points, start=1):
                    angle = calculate_angle(
                        landmarks[base],
                        landmarks[joint],
                        landmarks[tip]
                    )

                    if angle > 160:
                        fingers[i] = 1

                height, width, _ = frame.shape

                for point in landmarks:
                    x = int(point.x * width)
                    y = int(point.y * height)
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            pattern = "".join(map(str, fingers))

            cv2.putText(
                frame, "Fingers: " + pattern,
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2
            )

            cv2.imshow("Finger Detection Test", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        camera.release()
        cv2.destroyAllWindows()