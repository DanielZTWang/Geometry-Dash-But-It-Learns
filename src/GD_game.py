# Inputs
import pyautogui
import keyboard

# File pathing
from pathlib import Path

# Other
import numpy as np
import time

# Variables
frames_per_second = 240 # CHANGE TO MATCH GAME FPS
seconds_per_frame = 1 / frames_per_second
percent_file = Path("gd_data.txt")

# Game environment
class Game:
    def __init__(self):
        # Set starting values
        self.status = ()
        self.percent = 0.0
        self.best_percent = 0.0
        self.holding = False

    def reset(self):
        # Make sure bot isn't holding
        self.release()

        # Restart level with buffer
        pyautogui.press('r')
        time.sleep(0.05)

        # Read starting percentage
        self.status = self.get_status()
        self.percent = self.status[0]
        self.best_percent = self.percent
    
    def tap(self):
        pyautogui.mouseDown()
        time.sleep(0.01)
        pyautogui.mouseUp()

    def hold(self):
        if not self.holding:
            pyautogui.mouseDown()
        self.holding = True

    def release(self):
        if self.holding:
            pyautogui.mouseUp()
        self.holding = False
    
    def do_action(self, action):
        if action == "tap":
            self.tap()
        elif action == "hold":
            self.hold()
        elif action == "release":
            self.release()

    def get_status(self):
        try:
            # Reads the information and splits it into percentage, death, and completion status
            inp = percent_file.read_text().strip()
            perc_str, death_str, comp_str = inp.split(",")

            # Parses the information and returns it
            return (float(perc_str), death_str == "dead", comp_str == "complete")

        except Exception:
            return (self.percent, False, False)
        

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

            # Read current data
            status = self.get_status()
            self.percent = status[0]

            # Check if new best percentage is reached
            if self.percent > self.best_percent:
                self.best_percent = self.percent

            # Check if death has occurred
            if status[1]:
                self.release()
                return self.best_percent
            
            # Check if level is completed
            if status[2]:
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

                    print(f"Current percent: {self.percent:.2f}%")
                    print(f"Executed action: {event['action']} at {event['percent']:.2f}%")

                break

    def close(self):
        self.release()