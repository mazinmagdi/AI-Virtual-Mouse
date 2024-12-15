import cv2
import mediapipe as mp
import pyautogui
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def move_mouse(x, y):
    screen_width, screen_height = pyautogui.size()
    pyautogui.moveTo(x * screen_width, y * screen_height)

def click_mouse():
    pyautogui.click()

def scroll_screen(direction):
    if direction == 'up':
        pyautogui.scroll(10)
    elif direction == 'down':
        pyautogui.scroll(-10)

def zoom_screen(in_or_out):
    if in_or_out == 'in':
        pyautogui.hotkey('ctrl', '+')
    elif in_or_out == 'out':
        pyautogui.hotkey('ctrl', '-')

while True:
    success, frame = cap.read()
    if not success:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        for landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            x_index = index_tip.x
            y_index = index_tip.y
            x_thumb = thumb_tip.x
            y_thumb = thumb_tip.y
            x_middle = middle_tip.x
            y_middle = middle_tip.y


            distance = math.sqrt((x_index - x_thumb) ** 2 + (y_index - y_thumb) ** 2)

           
            if distance < 0.03:
                click_mouse()

            move_mouse(x_index, y_index)

            if y_thumb < y_middle:
                scroll_screen('up')
            elif y_thumb > y_middle:
                scroll_screen('down')

            thumb_index_distance = math.sqrt((x_index - x_thumb) ** 2 + (y_index - y_thumb) ** 2)
            if thumb_index_distance < 0.05:
                zoom_screen('in')
            elif thumb_index_distance > 0.1:
                zoom_screen('out')

    cv2.imshow("Virtual Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()