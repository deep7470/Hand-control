import cv2
import mediapipe as mp
import pyautogui

# Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

tip_ids = [4, 8, 12, 16, 20]

# Track current action to avoid repeated key presses
current_action = None

def release_keys():
    pyautogui.keyUp('right')
    pyautogui.keyUp('left')

print("🟢 SHOW Open Hand = Accelerate (Right Arrow)")
print("🟠 SHOW Fist = Brake/Reverse (Left Arrow)")
print("❌ Press Q to exit")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    lm_list = []
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape
            for id, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            if lm_list:
                fingers = []

                # Thumb (Check x position)
                if lm_list[tip_ids[0]][1] > lm_list[tip_ids[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Other fingers (Check y position)
                for i in range(1, 5):
                    if lm_list[tip_ids[i]][2] < lm_list[tip_ids[i] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total = fingers.count(1)

                # GESTURE: OPEN HAND = ACCELERATE
                if total == 5:
                    if current_action != "accelerate":
                        release_keys()
                        pyautogui.keyDown('right')
                        current_action = "accelerate"
                        print("🚗 Accelerating")

                # GESTURE: FIST = BRAKE
                elif total == 0:
                    if current_action != "brake":
                        release_keys()
                        pyautogui.keyDown('left')
                        current_action = "brake"
                        print("🛑 Braking")

                else:
                    if current_action is not None:
                        release_keys()
                        current_action = None
                        print("❎ No action")

                cv2.putText(frame, f"Fingers: {total}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    else:
        # No hand detected = release keys
        if current_action is not None:
            release_keys()
            current_action = None
            print("❎ No hand - released all keys")

    cv2.imshow("Hill Climb Gesture Control", frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        release_keys()
        break

cap.release()
cv2.destroyAllWindows()
