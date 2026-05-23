# Imports
import random
import copy

# Define possible actions
actions = ["tap"]
#actions = ["tap", "hold", "release"]

def create_random_genome(max_events = 10, max_percent = 20.0):
    genome = []

    # Append each event to the genome with random percentage and action
    for _ in range(random.randint(1, max_events)):
        event = {
            "percent": round(random.uniform(0, max_percent), 2),
            "action": random.choice(actions)
        }
        genome.append(event)
    
    return fix_genome(genome)

def fix_genome(genome):
    fixed_genome = []
    seen_percents = set()

    # Checks that there are no duplicate percentages and keeps the genome sorted by percentage
    for event in sorted(genome, key = lambda event: event["percent"]):
        if event["percent"] not in seen_percents:
            fixed_genome.append(event)
            seen_percents.add(event["percent"])

    return fixed_genome

def mutate_genome(genome, mutation_rate = 0.10, add_rate = 0.15, remove_rate = 0.10, min_percent = 0.0, max_percent = 100.0):
    new_genome = copy.deepcopy(genome)

    mutate_lo = max(0, min_percent - 1.5) 
    mutate_hi = min(100.0, max_percent + 1.5)

    # Mutate existing events
    for event in new_genome:
        if event["percent"] >= mutate_lo and event["percent"] <= mutate_hi:
            if random.random() < mutation_rate:
                event["percent"] += random.uniform(-0.4, 0.4)
                event["percent"] = round(event["percent"], 2)

            if random.random() < mutation_rate:
                event["action"] = random.choice(actions)

    # Add a new event
    if random.random() < add_rate:
        new_genome.append({
            "percent": round(random.uniform(mutate_lo, mutate_hi), 2),
            "action": random.choice(actions)
        })

    # Remove an event
    if random.random() < remove_rate and len(new_genome) > 1:
        r_event = random.randrange(len(new_genome))

        # Check if event is in the mutation range before removing
        if new_genome[r_event]["percent"] >= mutate_lo and new_genome[r_event]["percent"] <= mutate_hi:
            new_genome.pop(r_event)
    
    return fix_genome(new_genome)

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

    return fix_genome(new_genome)

def create_child(parent1, parent2, save_mark, max_percent):
    child = []
    p1, p2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
    i, j = 0, 0

    # Pick better parent
    if p1["fitness"] > p2["fitness"]:
        better = p1
    else:        
        better = p2
    
    # Save events from the better parent
    while i < len(better["genome"]) and better["genome"][i]["percent"] <= save_mark:
        child.append(copy.deepcopy(better["genome"][i]))
        i += 1
    
    # Remove events before the save mark
    while len(p2["genome"]) > 0 and p2["genome"][0]["percent"] <= save_mark:
        p2["genome"].pop(0)
    while len(p1["genome"]) > 0 and p1["genome"][0]["percent"] <= save_mark:
        p1["genome"].pop(0)

    # Crossover the remainder of the parents and mutate the child
    mutated_child = crossover(p1["genome"], p2["genome"])
    mutated_child = mutate_genome(
        mutated_child, 
        mutation_rate = 0.1, 
        add_rate = 0.15, 
        remove_rate = 0.10, 
        min_percent = save_mark, 
        max_percent = min(max(p1["fitness"], p2["fitness"]), max_percent)
    )
    
    # Combine the saved events with the mutated events
    child.extend(mutated_child)

    return fix_genome(child)