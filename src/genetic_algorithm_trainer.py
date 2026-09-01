from GD_game import Game
from genome import create_random_genome, create_child
from config import POPULATION_SIZE, GENERATIONS, MAX_EVENTS, INITIAL_START_PERCENT, INITIAL_MAX_PERCENT, MUTATION_RANGE, SAVE_PATH

import os
import json
import keyboard

def save_genome(genome, fitness, path):
    """
    Save a genome and its fitness score to a JSON file.

    Args:
        genome: The list of input events that make up the genome.
        fitness: The farthest percentage reached by this genome.
        path: The file path where the genome should be saved.
    """
    with open(path, "w") as f:
        json.dump({"fitness": fitness, "genome": genome}, f, indent = 4)

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

def evaluate_population(game, population):
    """
    Run every genome in the current population and record the farthest
    percentage reached before dying, or 100.0 if the level is completed.

    Args:
        game: The Game object used to control/read Geometry Dash.
        population: A list of genomes.

    Returns:
        A list of dictionaries sorted from best fitness to worst fitness.
        Each dictionary has:
            {
                "genome": genome,
                "fitness": fitness
            }
    """
    res = []

    for i, genome in enumerate(population):
        print(f"Testing genome {i + 1}/{len(population)}")

        fitness = game.run_genome(genome)
        res.append({"genome": genome, "fitness": fitness})

        if fitness == 100:
            return res

        print(f"Fitness: {fitness:.2f}%")
        print("Genome:", genome)
        print("-" * 40)
    
    res.sort(key = lambda item: item["fitness"], reverse = True)

    return res

def generate_population(new_population, best_genome):
    """
    Fill the next generation with children based on the best genome.

    The early part of the best genome is preserved up to save_mark.
    New/mutated events are generated around the current best/death area.

    Args:
        new_population: The partially built next generation.
        best_genome: A dictionary containing the best genome and its fitness.

    Returns:
        A full population list for the next generation.
    """
    while len(new_population) < POPULATION_SIZE:
        save_mark = max(0, best_genome["fitness"] - MUTATION_RANGE)

        child = create_child(best_genome, save_mark, best_genome["fitness"] + MUTATION_RANGE)
        new_population.append(child)

    return new_population

def make_next_generation(res):
    """
    Create the next generation from the current generation's results.

    Args:
        res: The sorted population results from evaluate_population().

    Returns:
        A new population of genomes.
    """
    best_genome = res[0]
    new_population = [best_genome["genome"]]

    return generate_population(new_population, best_genome)

def process_choice(choice):
    """
    Create the initial population based on the user's start choice.

    If the user chooses 'n', training starts from scratch with a random
    population.

    If the user chooses 'c', the program tries to load the saved best genome.
    If a saved genome exists, the initial population is built around that
    genome. If no saved genome exists, the program falls back to a new random
    population.

    Args:
        choice: The user's menu choice.
            'n' means start new.
            'c' means continue from the saved best genome.

    Returns:
        tuple: (population, best_overall_fitness, best_overall_genome)

        population:
            The starting population for training.

        best_overall_fitness:
            The best fitness known at the start of training.

        best_overall_genome:
            The genome with the best known fitness, or None.
    """
    if choice == 'n':
        population = [create_random_genome(MAX_EVENTS, INITIAL_START_PERCENT, INITIAL_START_PERCENT + INITIAL_MAX_PERCENT) for _ in range(POPULATION_SIZE)]
            
        best_overall_fitness = INITIAL_START_PERCENT
        best_overall_genome = None

    else:
        loaded_data = load_best_genome(SAVE_PATH)

        if loaded_data is None:
            print("No saved genome found.")
            
            population = [create_random_genome(MAX_EVENTS, INITIAL_START_PERCENT, INITIAL_START_PERCENT + INITIAL_MAX_PERCENT) for _ in range(POPULATION_SIZE)]
                        
            best_overall_fitness = INITIAL_START_PERCENT
            best_overall_genome = None
        else:
            genome, fitness = loaded_data

            best_overall_fitness = fitness
            best_overall_genome = genome

            best_genome = {"genome": genome, "fitness": fitness}
            population = make_next_generation([best_genome])

            print(f"Loaded saved genome with fitness: {fitness:.2f}%")

    return population, best_overall_fitness, best_overall_genome

def main():
    """
    Run the genetic algorithm training loop.

    The user first chooses whether to start from a new random population or
    continue from the saved best genome.

    The best genome is saved to SAVE_PATH whenever it reaches a new
    all-time-best fitness.
    """
    os.makedirs("genomes", exist_ok = True)

    game = Game()

    while True:
        choice = input("Enter 'n' to start new or 'c' to continue from the currently saved best genome: ").strip().lower()
        if (choice == 'n' or choice == 'c'):
            break

        print("Invalid input.")

    population, best_overall_fitness, best_overall_genome = process_choice(choice)

    print("Press \"z\" to start training.")
    while True:
        if keyboard.is_pressed("z"):
            break

    try:
        for generation in range(1, GENERATIONS + 1):
            if keyboard.is_pressed("x"):
                print("Training terminated by user.")
                break
            
            print(f"Generation {generation}/{GENERATIONS}")
            print("=" * 40)

            res = evaluate_population(game, population)

            print(f"Best fitness this generation: {res[0]['fitness']:.2f}%")
            print(f"Average fitness: {sum(item['fitness'] for item in res) / len(res):.2f}%")
            print(f"Best genome: {res[0]['genome']}")

            if res[0]["fitness"] > best_overall_fitness:
                best_overall_fitness = res[0]["fitness"]
                best_overall_genome = res[0]["genome"]

                save_genome(best_overall_genome, best_overall_fitness, SAVE_PATH)
                print(f"New best genome saved with fitness: {best_overall_fitness:.2f}%")
            
            if best_overall_fitness >= 100.0:
                print("Level complete")
                break

            population = make_next_generation(res)
    finally:
        print("Completed training")
        game.close()
        exit()
    
if __name__ == "__main__":
    main()
    # python src/genetic_algorithm_trainer.py