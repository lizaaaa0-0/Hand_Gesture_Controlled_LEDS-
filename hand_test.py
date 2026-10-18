
import cv2
import mediapipe as mp
import time
from pathlib import Path

model_path = str(Path(__file__).with_name("hand_landmarker.task"))

BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = mp.tasks.vision.HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

with mp.tasks.vision.HandLandmarker.create_from_options(options) as landmarker: 
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open webcam.")
    else:
        print("Show your hand to the camera. Press Q to quit.")

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
            if result.hand_landmarks:
                landmarks = result.hand_landmarks[0]
                height, width, _ = frame.shape

                for point in landmarks:
                    x = int(point.x * width)
                    y = int(point.y * height)
                    cv2.circle(frame, (x, y), 6, (0, 255, 0), -1)
                    cv2.putText(
                    frame, "HAND DETECTED!",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2
                )

            cv2.imshow("Hand Tracking Test", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        camera.release()
        cv2.destroyAllWindows()