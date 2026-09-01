from config import DATA_FILE

import pyautogui
import keyboard
import time

class Game:
    """
    Controls the Geometry Dash game state for the bot.

    This class reads game state from a data file written by the PercentageReader mod.
    The expected file format is:

        percent,death_status,completion_status

    Example:

        3.42,alive,incomplete
        0.0,dead,incomplete
        100.0,alive,complete

    A genome is a list of timed input events, such as:

        [
            {"percent": 1.5, "action": "tap"},
            {"percent": 3.8, "action": "hold"},
            {"percent": 4.2, "action": "release"}
        ]

    The game executes each event once when the current percentage reaches
    that event's percentage.
    """
    
    def __init__(self):
        """
        Initialize tracked game state.

        percent stores the current level percent.
        best_percent stores the farthest percent reached during the current genome.
        holding tracks whether the bot is currently holding input down.
        """
        self.status = ()
        self.percent = 0.0
        self.best_percent = 0.0
        self.holding = False

    def reset(self):
        """
        Reset the Geometry Dash level and initialize percentage tracking.
        """
        self.release()

        pyautogui.press('r')
        time.sleep(0.05)

        self.status = self.get_status()
        self.percent = self.status[0]
        self.best_percent = self.percent
    
    def tap(self):
        """
        Perform a tap input.
        """
        pyautogui.mouseDown()
        time.sleep(0.005)
        pyautogui.mouseUp()

        self.holding = False

    def hold(self):
        """
        Perform a holding input.

        If the bot is already holding, this avoids sending another mouseDown.
        """
        if not self.holding:
            pyautogui.mouseDown()

        self.holding = True

    def release(self):
        """
        Release held input if the bot is currently holding.
        """
        if self.holding:
            pyautogui.mouseUp()

        self.holding = False
    
    def do_action(self, action):
        """
        Execute a genome action.
        """
        if action == "tap":
            self.tap()
        elif action == "hold":
            self.hold()
        elif action == "release":
            self.release()

    def get_status(self):
        """
        Read the current game status from DATA_FILE.

        Returns:
            tuple: (percent, dead, complete)

            percent: float
            dead: bool
            complete: bool

        If the file cannot be read or parsed, the previous percent is reused
        and the game is assumed to still be alive/incomplete.
        """
        try:
            inp = DATA_FILE.read_text().strip()
            perc_str, death_str, comp_str = inp.split(",")

            return (float(perc_str), death_str == "dead", comp_str == "complete")

        except Exception:
            return (self.percent, False, False)

    def check_if_new_best(self):
        """
        Update best_percent if the current percent is farther than before.
        """
        if self.percent > self.best_percent:
            self.best_percent = self.percent

    def check_status(self, status):
        """
        Check whether the current genome attempt should end.

        status[1] = death status
        status[2] = completion status

        Returns:
            best_percent if the player died.
            100.0 if the level was completed.
            -1 if the attempt should continue.
        """
        if status[1]:
            self.release()
            return self.best_percent
        
        if status[2]:
            self.release()
            return 100.0

        return -1

    def execute_events(self, genome, next_event_index):
        """
        Execute all genome events whose percentage has been reached.

        Args:
            genome: list of event dictionaries.
            next_event_index: index of the next event that has not run yet.

        Returns:
            int: updated next_event_index.
        """
        while next_event_index < len(genome):
            event = genome[next_event_index]

            if self.percent >= event["percent"]:
                self.do_action(event["action"])
                next_event_index += 1
            else:
                break

        return next_event_index

    def run_genome(self, genome):
        """
        Run one genome attempt and return the farthest percentage reached
        before death, or 100.0 if the level is completed.
        """
        self.reset()

        genome = sorted(genome, key = lambda event: event["percent"])
        next_event_index = 0
        
        while True:
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
        """
        Clean up input state when training ends.
        """
        self.release()