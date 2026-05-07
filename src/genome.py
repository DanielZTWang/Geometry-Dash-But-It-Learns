# Imports
import random
import copy

# Define possible actions
actions = ["tap", "hold", "release"]

def create_random_genome(max_events = 10, max_percent = 20.0):
    genome = []

    # Append each event to the genome with random percentage and action
    for _ in range(random.randint(1, max_events)):
        event = {
            "percent": round(random.uniform(0, max_percent), 2),
            "action": random.choice(actions)
        }
        genome.append(event)

    # Keep the genome sorted by percentage
    genome.sort(key = lambda event: event["percent"])
    
    return genome

def mutate_genome(genome, mutation_rate = 0.1, add_rate = 0.15, remove_rate = 0.10, max_percent = 20.0):
    new_genome = copy.deepcopy(genome)

    # Mutate existing events
    for event in new_genome:
        if random.random() < mutation_rate:
            event["percent"] += random.uniform(-0.4, 0.4)
            event["percent"] = round(event["percent"], 2)
        
        if random.random() < mutation_rate:
            event["action"] = random.choice(actions)

    # Add a new event
    if random.random() < add_rate:
        new_genome.append({
            "percent": round(random.uniform(0.5, max_percent), 2),
            "action": random.choice(actions)
        })

    # Remove an event
    if random.random() < remove_rate and len(new_genome) > 1:
        new_genome.pop(random.randrange(len(new_genome)))

    # Keep the genome sorted by percentage
    new_genome.sort(key = lambda event: event["percent"])
    
    return new_genome

def crossover(genome1, genome2):
    new_genome = []
    i, j = 0, 0

    # Iterate through both genomes and merge based on percentage
    while i < len(genome1) and j < len(genome2):
        if genome1[i]["percent"] < genome2[j]["percent"]:
            new_genome.append(copy.deepcopy(genome1[i]))
            i += 1
        else:
            new_genome.append(copy.deepcopy(genome2[j]))
            j += 1

    # Add remaining events from either parent
    while i < len(genome1):
        new_genome.append(copy.deepcopy(genome1[i]))
        i += 1
    while j < len(genome2):
        new_genome.append(copy.deepcopy(genome2[j]))
        j += 1

    # Keep the genome sorted by percentage
    new_genome.sort(key = lambda event: event["percent"])

    return new_genome