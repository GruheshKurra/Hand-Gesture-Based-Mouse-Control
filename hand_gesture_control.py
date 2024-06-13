import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

screen_width, screen_height = pyautogui.size()

def distance(p1, p2):
    return np.linalg.norm(np.array([p1.x, p1.y]) - np.array([p2.x, p2.y]))

# Smoothing parameters
prev_x, prev_y = 0, 0
alpha = 0.7

# Click tracking
left_click_flag = False
right_click_flag = False
click_time = 0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    h, w, _ = frame.shape

    # Convert the frame color to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hands
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            # Determine if it's the left or right hand
            if handedness.classification[0].label == 'Left':
                # Left hand for left click
                left_index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                left_index_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                left_thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                if distance(left_index_tip, left_thumb_tip) < 0.05:
                    if not left_click_flag and time.time() - click_time > 0.5:
                        pyautogui.click(button='left')
                        left_click_flag = True
                        click_time = time.time()
                else:
                    left_click_flag = False

            elif handedness.classification[0].label == 'Right':
                # Right hand for cursor movement and right click
                right_index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                right_index_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                right_thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                # Smooth the cursor movement
                screen_x = np.interp(right_index_tip.x * w, (0, w), (0, screen_width))
                screen_y = np.interp(right_index_tip.y * h, (0, h), (0, screen_height))
                screen_x = alpha * prev_x + (1 - alpha) * screen_x
                screen_y = alpha * prev_y + (1 - alpha) * screen_y
                prev_x, prev_y = screen_x, screen_y
                pyautogui.moveTo(screen_x, screen_y)

                if distance(right_index_tip, right_thumb_tip) < 0.05:
                    if not right_click_flag and time.time() - click_time > 0.5:
                        pyautogui.click(button='right')
                        right_click_flag = True
                        click_time = time.time()
                else:
                    right_click_flag = False

            # Draw hand landmarks on the frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
