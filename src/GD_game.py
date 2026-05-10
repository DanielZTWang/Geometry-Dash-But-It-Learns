# Inputs
import pyautogui
import keyboard

# Screen reading
import pytesseract
import cv2
import mss

# File pathing
from pathlib import Path

# Other
import numpy as np
import time

# Variables
framesPerSecond = 240 # CHANGE TO MATCH GAME FPS
secondsPerFrame = 1 / framesPerSecond
screenWidth, screenHeight = pyautogui.size()
centerX = screenWidth // 2
centerY = screenHeight // 2
percentageBox = {"left": 1640, "top": 185, "width": 230, "height": 60} # CHANGE TO MATCH PERCENTAGE BOX COORDINATES

# Game environment
class Game:
    def __init__(self):
        # Set up tesseract path
        filePath = Path("Tesseract-OCR").joinpath("tesseract.exe")
        pytesseract.pytesseract.tesseract_cmd = str(filePath.absolute())

        # Create screenshot object
        self.sct = mss.mss()
        
        # Set starting values
        self.percent = 0.0
        self.prev_percent = 0.0
        self.best_percent = 0.0
        self.holding = False

    def reset(self):
        # Make sure bot isn't holding
        self.release()

        # Restart level with buffer
        pyautogui.press('r')
        time.sleep(0.05)

        # Read starting percentage
        self.percent = self.get_percentage()
        self.prev_percent = self.percent
        self.best_percent = self.percent
    
    def tap(self):
        pyautogui.mouseDown(x=centerX, y=centerY)
        time.sleep(0.01)
        pyautogui.mouseUp(x=centerX, y=centerY)

    def hold(self):
        if not self.holding:
            pyautogui.mouseDown(x=centerX, y=centerY)
        self.holding = True

    def release(self):
        if self.holding:
            pyautogui.mouseUp(x=centerX, y=centerY)
        self.holding = False
    
    def do_action(self, action):
        if action == "tap":
            self.tap()
        elif action == "hold":
            self.hold()
        elif action == "release":
            self.release()

    def get_percentage(self):
        # Reads the percentage as a string
        img = np.array(self.sct.grab(percentageBox))
        inp = pytesseract.image_to_string(
            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY),
            lang = "eng",
            config = "--psm 7 -c tessedit_char_whitelist=0123456789.%"
        )

        # Clean up the string
        inp = inp.strip().replace('%', '').replace('O', '0').replace('o', '0')
        inp = "".join(char for char in inp if char.isdigit() or char == ".")

        # Convert string percent to float
        try: percent = float(inp)
        except: percent = self.percent

        return percent

    def run_genome(self, genome):
        # Reset the game state
        self.reset()

        genome = sorted(genome, key = lambda event: event["percent"])

        next_event_index = 0
        
        while True:
            # Check for forced stop
            if keyboard.is_pressed("x"):
                print("Training terminated by user.")
                break

            # Read current percentage
            self.prev_percent = self.percent
            self.percent = self.get_percentage()

            # Check if new best percentage is reached
            if self.percent > self.best_percent:
                self.best_percent = self.percent

            # Check if death has occurred
            if self.percent < self.prev_percent:
                self.release()
                return self.best_percent
            
            # Check if level is completed
            if self.percent >= 100:
                self.release()
                return 100.0
            
            # Iterate through the genome and perform actions
            while next_event_index < len(genome):
                # Get the next event
                event = genome[next_event_index]

                # Execute event and move to next event if percentage threshold is met
                if self.percent >= event["percent"]:
                    self.do_action(event["action"])
                    next_event_index += 1
                else:
                    break

    def close(self):
        self.release()