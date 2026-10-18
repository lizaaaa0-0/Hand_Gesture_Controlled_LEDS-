
import cv2
import mediapipe as mp
import serial
import time
import math
from pathlib import Path

# Change COM7 if your Arduino uses a different port
ARDUINO_PORT = "COM7"
BAUD_RATE = 9600

model_path = str(Path(__file__).with_name("hand_landmarker.task"))

arduino = None
camera = None

def calculate_angle(a, b, c):
    angle1 = math.atan2(a.y - b.y, a.x - b.x)
    angle2 = math.atan2(c.y - b.y, c.x - b.x)
    angle = abs(math.degrees(angle1 - angle2))

    if angle > 180:
        angle = 360 - angle

    return angle

try:
    # Connect to Arduino
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print("Arduino connected!")

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
            raise RuntimeError("Could not open webcam.")

        print("Show your hand. Press Q to quit.")

        previous_pattern = ""

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
                if calculate_angle(
                    landmarks[2], landmarks[3], landmarks[4]
                ) > 150:
                    fingers[0] = 1

                # Index, middle, ring and little fingers
                finger_points = [
                    (5, 6, 8),
                    (9, 10, 12),
                    (13, 14, 16),
                    (17, 18, 20)
                ]

                for i, (base, joint, tip) in enumerate(
                    finger_points, start=1
                ):
                    if calculate_angle(
                        landmarks[base],
                        landmarks[joint],
                        landmarks[tip]
                    ) > 160:
                        fingers[i] = 1

                height, width, _ = frame.shape

                for point in landmarks:
                    x = int(point.x * width)
                    y = int(point.y * height)
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            # No detected hand means all LEDs turn off
            pattern = "".join(map(str, fingers))

            # Send only when the pattern changes
            if pattern != previous_pattern:
                arduino.write((pattern + "\n").encode())
                print("LED pattern:", pattern)
                previous_pattern = pattern

            cv2.putText(
                frame, "LEDs: " + pattern,
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2
            )

            cv2.imshow("Hand Controlled LEDs", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

except serial.SerialException as error:
    print("Arduino connection error:", error)

except (RuntimeError, OSError) as error:
    print("Error:", error)

finally:
    if camera is not None:
        camera.release()

    cv2.destroyAllWindows()

    if arduino is not None and arduino.is_open:
        try:
            arduino.write(b"00000\n")
            arduino.close()
        except serial.SerialException:
            pass

    print("Program stopped. LEDs commanded off.")
