from config import ACTIONS

import random
import copy

def create_random_genome(max_events, min_percent, max_percent):
    """
    Create a random genome.

    A genome is a list of input events. Each event has:
        - percent: the level percentage where the action should happen
        - action: the input action to perform

    Example:
        [
            {"percent": 1.5, "action": "tap"},
            {"percent": 3.8, "action": "hold"},
            {"percent": 4.2, "action": "release"}
        ]

    Args:
        max_events: The maximum number of events the genome can contain.
        min_percent: The lowest percentage where random events can be placed.
        max_percent: The highest percentage where random events can be placed.

    Returns:
        A cleaned random genome.
    """
    genome = []

    for _ in range(random.randint(1, max_events)):
        event = {
            "percent": round(random.uniform(min_percent, max_percent), 1),
            "action": random.choice(ACTIONS)
        }
        genome.append(event)
    
    return fix_genome(genome)

def clean_actions(genome):
    """
    Remove action events that would have no useful effect.

    Args:
        genome: A genome sorted by percentage.

    Returns:
        A genome with unnecessary hold/release actions removed.
    """
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
    """
    Clean and sort a genome.

    Args:
        genome: A list of genome events.

    Returns:
        A cleaned genome.
    """
    fixed_genome = []
    seen_percents = set()

    for event in sorted(genome, key = lambda event: event["percent"]):
        if event["percent"] not in seen_percents:
            fixed_genome.append(event)
            seen_percents.add(event["percent"])

    fixed_genome = clean_actions(fixed_genome)

    return fixed_genome

def add_events(genome, max_events, low, high):
    """
    Add random events to a genome within a percentage range.

    Args:
        genome: The genome to add events to.
        low: The lowest percentage where a new event can be placed.
        high: The highest percentage where a new event can be placed.

    Returns:
        The genome with new random events added.
    """
    for _ in range(random.randint(0, max_events)):
        genome.append({
            "percent": round(random.uniform(low, high), 1),
            "action": random.choice(ACTIONS)
        })

    return genome

def mutate_tail(max_events, min_percent, max_percent):
    """
    Generate a new random genome tail within a mutation range.

    The tail is the part of a child genome after the saved section of the
    best genome. This lets the algorithm preserve earlier successful inputs
    while trying new actions near the current death/progress area.

    Args:
        min_percent: The lower bound of the mutation range.
        max_percent: The upper bound of the mutation range.

    Returns:
        A cleaned list of new random events in the mutation range.
    """
    mutate_lo = max(0, min_percent) 
    mutate_hi = min(100.0, max_percent)

    new_tail = []
    new_tail = add_events(new_tail, max_events, mutate_lo, mutate_hi)
    
    return fix_genome(new_tail)

def create_child(best_genome, max_events, save_mark, max_percent):
    """
    Create a child genome from the current best genome.

    The child keeps all events from the best genome up to save_mark, then
    generates a new random tail from save_mark to max_percent.

    Args:
        best_genome: A dictionary containing:
            {
                "genome": genome,
                "fitness": fitness
            }

        save_mark: The percentage up to which old events should be preserved.
        max_percent: The upper bound for generating new tail events.

    Returns:
        A cleaned child genome.
    """
    child = []
    
    cur_event = 0
    while cur_event < len(best_genome["genome"]) and best_genome["genome"][cur_event]["percent"] <= save_mark:
        child.append(copy.deepcopy(best_genome["genome"][cur_event]))
        cur_event += 1

    mutated_tail = mutate_tail(max_events, save_mark, max_percent)
    child.extend(mutated_tail)

    return fix_genome(child)