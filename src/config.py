from pathlib import Path

# Genetic algorithm settings
POPULATION_SIZE = 10
GENERATIONS = 1000
MAX_EVENTS = 20
INITIAL_MAX_PERCENT = 10.0
MUTATION_RANGE = 1.5 # CHANGE DEPENDING ON LEVEL
SAVE_PATH = "genomes/best_genome.json"

# Game data file
DATA_FILE = Path("gd_data.txt")

# Possible actions
ACTIONS = ["tap", "hold", "release"]