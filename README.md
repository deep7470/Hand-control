Hand Gesture Control

This project lets you control games using simple hand gestures detected through your webcam. It uses Mediapipe to track your hand, then simulates arrow-key inputs for actions like accelerating or braking in driving games.

#Features

1.Detects hand gestures in real time

2.Open hand triggers acceleration (Right Arrow)

3.Closed fist triggers braking (Left Arrow)

4.Automatically releases keys when no hand is detected

5.Works with any game that uses arrow keys
--------------------------------------------------------------------------------------------------------------------------
Requirements

Python 3.x

OpenCV

Mediapipe

PyAutoGUI

#Install dependencies with:

pip install opencv-python mediapipe pyautogui

#How to Run
python signlanguage.py


Keep your hand in front of the webcam and use gestures to control the game.
-----------------------------------------------------------------------------------------------------
Notes

Make sure your lighting is good so the hand is detected clearly.

Works best with one hand visible in the frame.


----------------------------------------------------------------------------------------------------------
