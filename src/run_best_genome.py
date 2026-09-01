from GD_game import Game
from config import SAVE_PATH

import os
import json
import keyboard

def load_best_genome(path):
    """
    Load a saved genome and its fitness score from a JSON file.

    Args:
        path: The file path to load from.

    Returns:
        None if the file does not exist.
        Otherwise, returns (genome, fitness).
    """
    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        data = json.load(f)

    return data["genome"], data["fitness"]

def main():
    """
    Load and repeatedly run the saved best genome.

    The genome is not mutated or changed here. This file only tests/replays the
    best genome found during training.
    """
    loaded_data = load_best_genome(SAVE_PATH)

    if loaded_data is None:
        print("No genome found.")
        exit()

    genome, fitness = loaded_data

    print(f"Loaded genome with saved fitness: {fitness:.2f}%")
    print("Genome:", genome)

    game = Game()

    print("Press \"z\" to start running.")
    while True:
        if keyboard.is_pressed("z"):
            break

    try:
        result = 0

        while result < 100:
            result = game.run_genome(genome)
            print(f"Run finished. Reached: {result:.2f}%")

    finally:
        game.close()

if __name__ == "__main__":
    main()
    # python src/run_best_genome.py