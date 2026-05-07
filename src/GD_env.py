# Env
from gymnasium import Env
from gymnasium.spaces import Discrete, Box

# Inputs
import pyautogui

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
class GameEnv(Env):
    def __init__(self):
        # Call parent initializer
        super().__init__()

        # Actions: Nothing, tap
        self.action_space = Discrete(2)

        # Observe current percentage
        self.observation_space = Box(
            low = np.array([0.0]),
            high = np.array([100.0]), 
            dtype = np.float32
        )

        # Create screenshot object
        self.sct = mss.mss()
        
        # Set starting values
        self.percent = 0.0
        self.prev_percent = 0.0
        self.best_percent = 0.0

        self.frame_count = 0
        self.stuck_frames = 0
        self.max_stuck_frames = 500

        self.holding = False

    def step(self, action):
        # Apply action
        if action == 0:
            pass
        elif action == 1:
            pyautogui.mouseDown(x = centerX, y = centerY)
            time.sleep(0.01)
            pyautogui.mouseUp(x = centerX, y = centerY)
        
        """ elif action == 2:
            if not self.holding:
                pyautogui.mouseDown(x=centerX, y=centerY)
                self.holding = True
        elif action == 3:
            if self.holding:
                pyautogui.mouseUp(x=centerX, y=centerY)
                self.holding = False """
        
        # Wait one frame
        time.sleep(secondsPerFrame)

        # Read new percentage
        self.prev_percent = self.percent
        self.frame_count += 1
        read_percent = False

        if self.frame_count % 3 == 0:
            self.percent = self.get_percentage()
            read_percent = True

        # Calculate progress made
        raw_progress = self.percent - self.prev_percent

        reward = 0.0
        terminated = False

        # Check if the bot has died
        if raw_progress < -0.1 and read_percent:
            reward -= 30
            terminated = True

        # Calculate reward otherwise
        else:
            progress = max(0.0, raw_progress)

            if read_percent:
                reward += progress
                
                # Update best percent
                if self.percent > self.best_percent:
                    self.best_percent = self.percent
                
                # Check if bot is stuck or dead
                if raw_progress <= 0.0001:
                    self.stuck_frames += 1
                else:
                    self.stuck_frames = 0

            if self.percent >= 100:
                reward += 100
                terminated = True
            elif self.stuck_frames >= self.max_stuck_frames:
                reward -= 30
                terminated = True
            else:
                terminated = False
        
        
        # Set return values
        truncated = False
        obs = np.array([self.percent], dtype=np.float32)
        info = {"percent": self.percent, 
                "best_percent": self.best_percent, 
            }

        return obs, reward, terminated, truncated, info

    def render(self):
        pass

    def reset(self, seed = None, options = None):
        super().reset(seed = seed)
        
        # Makes sure the bot isn't holding down after reset 
        if self.holding:
            pyautogui.mouseUp(x=centerX, y=centerY)
            self.holding = False

        # Restart level with buffer
        pyautogui.press('r')
        time.sleep(0.05)

        # Read starting percentage
        self.percent = self.get_percentage()
        self.prev_percent = self.percent
        self.frame_count = 0
        self.stuck_frames = 0

        # Set return values
        obs = np.array([self.percent], dtype=np.float32)
        info = {}

        return obs, info

    def get_percentage(self):
        # Set up tesseract path
        filePath = Path("Tesseract-OCR").joinpath("tesseract.exe")
        pytesseract.pytesseract.tesseract_cmd = str(filePath.absolute())
        
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
    
    """ def record_death_percent(self, percent):
        self.death_percents.append(percent)

        if len(self.death_percents) > 20:
            self.death_percents.pop(0)

        if len(self.death_percents) >= 5:
            avg_death_percent = sum(self.death_percents) / len(self.death_percents)
            close_deaths = 0

            for p in self.death_percents:
                if abs(p - avg_death_percent) < 0.2:
                    close_deaths += 1
            
            if close_deaths >= 3:
                self.stuck_death_percent = avg_death_percent """