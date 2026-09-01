from config import ACTIONS

import random
import copy

def create_random_genome(max_events, max_percent):
    genome = []

    # Append each event to the genome with random percentage and action
    for _ in range(random.randint(1, max_events)):
        event = {
            "percent": round(random.uniform(0, max_percent), 1),
            "action": random.choice(ACTIONS)
        }
        genome.append(event)
    
    return fix_genome(genome)

def clean_actions(genome):
    fixed_genome = []

    holding = False
    for event in genome:
        action = event["action"]

        if action == "hold":
            if holding:
                continue
            holding = True

        elif action == "release":
            if not holding:
                continue
            holding = False

        fixed_genome.append(event)

    return fixed_genome

def fix_genome(genome):
    fixed_genome = []
    seen_percents = set()

    # Checks that there are no duplicate percentages and keeps the genome sorted by percentage
    for event in sorted(genome, key = lambda event: event["percent"]):
        if event["percent"] not in seen_percents:
            fixed_genome.append(event)
            seen_percents.add(event["percent"])

    fixed_genome = clean_actions(fixed_genome)

    return fixed_genome

def add_events(genome, low, high):
    for _ in range(random.randint(1, 15)):
        genome.append({
            "percent": round(random.uniform(low, high), 1),
            "action": random.choice(ACTIONS)
        })

    return genome

def mutate_tail(min_percent, max_percent):
    mutate_lo = max(0, min_percent) 
    mutate_hi = min(100.0, max_percent)

    new_tail = []
    new_tail = add_events(new_tail, mutate_lo, mutate_hi)
    
    return fix_genome(new_tail)

def create_child(best_genome, save_mark, max_percent):
    child = []
    
    # Save events up to the save mark
    cur_event = 0
    while cur_event < len(best_genome["genome"]) and best_genome["genome"][cur_event]["percent"] <= save_mark:
        child.append(copy.deepcopy(best_genome["genome"][cur_event]))
        cur_event += 1

    mutated_tail = mutate_tail(save_mark, max_percent)
    child.extend(mutated_tail)

    return fix_genome(child)