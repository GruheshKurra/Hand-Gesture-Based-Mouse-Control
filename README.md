# Hand Gesture-Based Mouse Control

This project uses MediaPipe, OpenCV, and PyAutoGUI to control the mouse cursor and perform click actions using hand gestures. The right hand is used for cursor movement, the left hand for left clicks, and the right hand for right clicks.

## Features
- **Cursor Movement**: Move the cursor using the right hand's index finger.
- **Left Click**: Close the left hand (all fingers close to the palm) to perform a left click.
- **Right Click**: Close the right hand (all fingers close to the palm) to perform a right click.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/hand-gesture-mouse-control.git
   cd hand-gesture-mouse-control
   ```
2. **Install Dependencies**
   Make sure you have Python 3.x installed. Then, install the required libraries:
   ```bash
   pip install opencv-python mediapipe pyautogui numpy
   ```

## Usage

1. **Run the Script**
   ```bash
   python hand_gesture_mouse_control.py
   ```
2. **Control the Mouse**
- Cursor Movement: Move the cursor using the right hand's index finger.
- Left Click: Close the left hand (all fingers close to the palm) to perform a left click.
- Right Click: Close the right hand (all fingers close to the palm) to perform a right click.
