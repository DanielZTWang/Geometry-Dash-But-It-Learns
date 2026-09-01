# Game and genome imports
from GD_game import Game
from genome import create_random_genome, create_child

# File managing
import os
import json

# Input checking
import keyboard

# Variables
population_size = 10
generations = 1000
max_events = 20
save_threshold = 1.5 # CHANGE DEPENDING ON LEVEL
save_path = "genomes/best_genome.json"

def save_genome(genome, fitness, path):
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

def generate_population(new_population, elite):
    while len(new_population) < population_size:
        save_mark = max(0, elite["fitness"] - save_threshold)

        child = create_child(elite, save_mark, elite["fitness"] + save_threshold)
        new_population.append(child)

    return new_population

def make_next_generation(res):
    elite = res[0]
    new_population = []

    return generate_population(new_population, elite)

def main():
    os.makedirs("genomes", exist_ok = True)

    # Initialize the game
    game = Game()

    # Allow for manual start
    while True:
        if keyboard.is_pressed('z'): # CHANGE 'z' TO ANY KEY YOU WANT AS START
            break

    # Create the initial random population
    population = [create_random_genome(max_events, 10) for _ in range(population_size)]
    
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
        print("Completed training")
        game.close()
        exit()
    
if __name__ == "__main__":
    main()
    # python src/genetic_algorithm_trainer.py x