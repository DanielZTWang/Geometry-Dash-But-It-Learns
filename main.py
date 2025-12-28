# Inputs
import pyautogui

# Screen reading
import pytesseract
import cv2
from PIL import ImageGrab

# Other
import numpy as np
import random
import time

def get_percentage():
    pytesseract.pytesseract.tesseract_cmd ='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    
    while True:
        img = ImageGrab.grab(bbox = (1640, 185, 1870, 245))

        tesstr = pytesseract.image_to_string(
                cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY), 
                lang ='eng')
        
        print('percentage: ' + tesstr)

get_percentage()

# class GameEnv(Env):
#     def __init__(self):
#         # Actions: Nothing, tap, or hold (100ms, 200ms, 300ms, 400ms)
#         self.action_space = Discrete(6)
#         # Percentage array
#         self.observation_space = Box(low = np.array([0]), high = np.array([100]))
#         # Set start percentage
#         self.state = 0
#         # Set level length
#         self.level_length = 60

#     def step(self, action):
#         # Apply action
#         if action == 2:
#             pyautogui.click(x=1200, y=700)
#         elif action == 3:
#             pyautogui.mouseDown()
#             time.sleep(0.1)
#             pyautogui.mouseUp(x=1200, y=700)
#         elif action == 4:
#             pyautogui.mouseDown()
#             time.sleep(0.2)
#             pyautogui.mouseUp(x=1200, y=700)
#         elif action == 5:
#             pyautogui.mouseDown()
#             time.sleep(0.3)
#             pyautogui.mouseUp(x=1200, y=700)
#         elif action == 6:
#             pyautogui.mouseDown()
#             time.sleep(0.4)
#             pyautogui.mouseUp(x=1200, y=700)
#         else:
#             print("?")
        
#         # Reduce level length by 200ms
#         self.game_length -= 0.2

#         # Reward

#         # Check if level is complete
        


#     def render(self):
#         pass
#     def reset(self):
#         pass

