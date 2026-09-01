from config import DATA_FILE

import pyautogui
import keyboard
import time

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
        time.sleep(0.005)
        pyautogui.mouseUp()

        self.holding = False

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
            inp = DATA_FILE.read_text().strip()
            perc_str, death_str, comp_str = inp.split(",")

            # Parses the information and returns it
            return (float(perc_str), death_str == "dead", comp_str == "complete")

        except Exception:
            return (self.percent, False, False)

    def check_if_new_best(self):
        if self.percent > self.best_percent:
            self.best_percent = self.percent

    def check_status(self, status):
        # Check if death has occurred
        if status[1]:
            self.release()
            return self.best_percent
        
        # Check if level is completed
        if status[2]:
            self.release()
            return 100.0

        return -1

    def execute_events(self, genome, next_event_index):
        # Iterate through the genome and perform actions
        while next_event_index < len(genome):
            event = genome[next_event_index]

            # Execute event and move to next event if percentage threshold is met
            if self.percent >= event["percent"]:
                self.do_action(event["action"])
                next_event_index += 1
            else:
                break

        return next_event_index

    def run_genome(self, genome):
        self.reset()

        genome = sorted(genome, key = lambda event: event["percent"])
        next_event_index = 0
        
        while True:
            # Check for forced stop
            if keyboard.is_pressed("x"):
                print("Training terminated by user.")
                break

            status = self.get_status()
            self.percent = status[0]

            self.check_if_new_best()

            res = self.check_status(status)
            if res != -1:
                return res
            
            next_event_index = self.execute_events(genome, next_event_index)

    def close(self):
        self.release()