# Game and genome imports
from GD_game import Game
from genome import create_random_genome, create_child

# File managing
import os
import json

# Input checking
import keyboard

# Other
import random

# Variables
population_size = 10
generations = 100
elite_count = 4
max_events = 20
max_percent = 20.0
save_path = "genomes/best_genome.json"

def save_genome(genome, fitness, path):
    # Save the genome and its fitness to a JSON file
    with open(path, "w") as f:
        json.dump({"fitness": fitness, "genome": genome}, f, indent = 4)

def load_best_genome(path):
    # Check if file exists
    if not os.path.exists(path):
        return None

    # Load the best genome and its fitness from a JSON file
    with open(path, "r") as f:
        data = json.load(f)

    return data["genome"], data["fitness"]

def evaluate_population(game, population):
    res = []

    # Evaluate each genome in the population and store its fitness
    for i, genome in enumerate(population):
        print(f"Testing genome {i + 1}/{len(population)}")

        # Run the genome and get its fitness
        fitness = game.run_genome(genome)
        res.append({"genome": genome, "fitness": fitness})

        print(f"Fitness: {fitness:.2f}%")
        print("Genome:", genome)
        print("-" * 40)
    
    res.sort(key = lambda item: item["fitness"], reverse = True)
    return res

def make_next_generation(res):
    # Define a threshold for how much of a genome should be saved in relation to best fitness
    save_threshold = 1 # CHANGE DEPENDING ON LEVEL

    # Produce a population of elite genomes from the previous generation
    elites = res[:elite_count]
    new_population = [elite["genome"] for elite in elites]

    # Mutate the elite genomes until full population
    while len(new_population) < population_size:
        # Select two random elite genomes as parents
        parent1 = random.choice(elites)
        parent2 = random.choice(elites)

        # Determine the mark to begin mutating the child genome
        if parent1["fitness"] < parent2["fitness"]:
            save_mark = max(0, parent1["fitness"] - save_threshold)
        else:
            save_mark = max(0, parent2["fitness"] - save_threshold)

        # Create the child genome up to the save mark
        child = create_child(parent1, parent2, save_mark = save_mark, max_percent = max_percent)

        # Append the child genome to the new population
        new_population.append(child)

    return new_population

def main():
    # Create a genome folder
    os.makedirs("genomes", exist_ok = True)

    # Initialize the game
    game = Game()

    # Allow for manual start
    while True:
        if keyboard.is_pressed('z'): # CHANGE 'z' TO ANY KEY YOU WANT AS START
            break

    # Create the initial random population
    population = [create_random_genome(max_events, max_percent) for _ in range(population_size)]
    
    # Initialize fitness and genome tracking variables
    best_overall_fitness = 0.0
    best_overall_genome = None

    try:
        for generation in range(1, generations + 1):
            # Check for forced stop
            if keyboard.is_pressed("x"):
                print("Training terminated by user.")
                break
            
            print(f"Generation {generation}/{generations}")
            print("=" * 40)

            # Evaluate the current population and store the results
            res = evaluate_population(game, population)

            print(f"Best fitness this generation: {res[0]['fitness']:.2f}%")
            print(f"Average fitness: {sum(item['fitness'] for item in res) / len(res):.2f}%")
            print(f"Best genome: {res[0]['genome']}")

            # Check if the best genome of this population has a better fitness than the current best
            if res[0]["fitness"] > best_overall_fitness:
                # Update the best overall fitness and genome
                best_overall_fitness = res[0]["fitness"]
                best_overall_genome = res[0]["genome"]

                # Save the best genome to a file
                save_genome(best_overall_genome, best_overall_fitness, save_path)
                print(f"New best genome saved with fitness: {best_overall_fitness:.2f}%")
            
            # Check if the bot has beat the level
            if best_overall_fitness >= 100.0:
                print("Level complete")
                break

            # Create the next generation of genomes
            population = make_next_generation(res)
    finally:
        game.close()
    
if __name__ == "__main__":
    main()
    # python src/genetic_algorithm_trainer.py