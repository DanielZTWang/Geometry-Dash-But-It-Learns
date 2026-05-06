# Env
from gymnasium import Env
from gymnasium.spaces import Discrete, Box

# Inputs
import pyautogui

# Screen reading
import pytesseract
import cv2
from PIL import ImageGrab

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

# Game environment
class GameEnv(Env):
    def __init__(self):
        # Call parent initializer
        super().__init__()

        # Actions: Nothing, tap, hold, release
        self.action_space = Discrete(4)

        # Observe current percentage
        self.observation_space = Box(
            low = np.array([0.0, 0.0]),
            high = np.array([100.0, 1.0]), 
            dtype=np.float32
        )
        
        # Set starting values
        self.percent = 0.0
        self.prev_percent = 0.0
        self.best_percent = 00.0

        self.stuck_frames = 0
        self.max_stuck_frames = 500

        self.holding = False

    def step(self, action):
        # Apply action
        if action == 0:
            pass
        elif action == 1:
            pyautogui.click(x=centerX, y=centerY)
        elif action == 2:
            if not self.holding:
                pyautogui.mouseDown(x=centerX, y=centerY)
                self.holding = True
        elif action == 3:
            if self.holding:
                pyautogui.mouseUp(x=centerX, y=centerY)
                self.holding = False
        
        # Wait one frame
        time.sleep(secondsPerFrame)

        # Read new percentage
        self.prev_percent = self.percent
        self.percent = self.get_percentage()

        # Calculate progress made
        raw_progress = self.percent - self.prev_percent

        # Check if the bot has died
        if (raw_progress < -0.1):

            reward = -10
            terminated = True

        # Calculate reward otherwise
        else:
            progress = max(0.0, raw_progress)
            reward = progress * 10

            # Reward for new best
            if (self.percent > self.best_percent):
                self.best_percent = self.percent
                reward += 1
            
            # Check if bot is stuck or dead
            if raw_progress <= 0.0001:
                self.stuck_frames += 1
            else:
                self.stuck_frames = 0

            if self.percent >= 100:
                reward += 100
                terminated = True
            elif self.stuck_frames >= self.max_stuck_frames:
                reward -= 10
                terminated = True
            else:
                terminated = False
        
        
        # Set return values
        truncated = False
        obs = np.array([self.percent, float(self.holding)], dtype=np.float32)
        info = {"percent": self.percent, "best_percent": self.best_percent}

        return obs, reward, terminated, truncated, info

    def render(self):
        pass

    def reset(self, seed = None, options = None):
        super().reset(seed = seed)
        
        # Makes sure the bot isn't holding down after reset 
        if self.holding:
            pyautogui.mouseUp(x=centerX, y=centerY)
            self.holding = False

        # Restart level with 2 frame buffer
        pyautogui.press('r')
        time.sleep(secondsPerFrame * 2)

        # Read starting percentage
        self.percent = self.get_percentage()
        self.prev_percent = self.percent
        self.stuck_frames = 0

        # Set return values
        obs = np.array([self.percent, float(self.holding)], dtype=np.float32)
        info = {}

        return obs, info

    def get_percentage(self):
        # Set up tesseract path
        filePath = Path("Tesseract-OCR").joinpath("tesseract.exe")
        pytesseract.pytesseract.tesseract_cmd = str(filePath.absolute())
        
        # Reads the percentage as a string
        img = ImageGrab.grab(bbox = (1640, 185, 1870, 245)) # NEEDS TO MATCH PERCENTAGE BOX COORDINATES
        inp = pytesseract.image_to_string(
            cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY), 
            lang = 'eng'
        ) 

        # Clean up the string
        inp = inp.strip().replace('%', '').replace('O', '0').replace('o', '0')
        for char in inp:
            if not char.isdigit() and char != '.':
                inp = inp.replace(char, '')

        # Convert string percent to float
        try: percent = float(inp)
        except: percent = self.percent

        return percent
