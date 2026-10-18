# Hand Gesture-Controlled LED System

A computer-vision project that uses hand gestures to control five LEDs connected to an Arduino Uno.

## Features

* Real-time webcam video capture
* Hand landmark detection using MediaPipe
* Finger detection using Python
* Serial communication between Python and Arduino
* Independent control of five LEDs using hand gestures

## Hardware

* Arduino Uno
* 5 LEDs and 5 current-limiting resistors
* Breadboard and jumper wires
* USB cable
* Laptop webcam

## Software and Libraries

* Python
* OpenCV
* MediaPipe
* PySerial
* Arduino IDE

## How It Works

1. The webcam captures video of the user's hand.
2. OpenCV processes the video frames.
3. MediaPipe detects 21 hand landmarks.
4. Python determines which fingers are raised.
5. The finger states are converted into a five-digit binary pattern.
6. PySerial sends the pattern to the Arduino over USB.
7. The Arduino switches the corresponding LEDs on or off.

## LED Pin Mapping

| Finger | Arduino Pin |
| ------ | ----------- |
| Thumb  | D2          |
| Index  | D3          |
| Middle | D4          |
| Ring   | D5          |
| Little | D6          |

Each LED uses its own current-limiting resistor.

## Example Gestures

| Gesture                               | Pattern |
| ------------------------------------- | ------- |
| Index finger raised                   | `01000` |
| Index, middle and ring fingers raised | `01110` |
| All five fingers raised               | `11111` |
| Closed fist or no detected hand       | `00000` |

The bit order is thumb, index, middle, ring and little finger.

## Setup

1. Install Python, Git and the Arduino IDE.

2. Install the required packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Place `hand_landmarker.task` in the project folder.

4. Upload the Arduino sketch to your Arduino Uno.

5. Close the Arduino Serial Monitor.

6. Update the COM port in `hand_led.py` to match your Arduino.

7. Run the project:

   ```bash
   python hand_led.py
   ```

Press `Q` to exit the webcam window.

## Future Improvements

* Gesture-controlled servo motors
* A cardboard robotic hand
* RGB LED control
* Additional hand gestures and interaction modes

## Author

Built as a hands-on project combining computer vision, Python programming and Arduino electronics.
