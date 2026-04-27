#!/usr/bin/env python3
"""Basic example: Evolving optimal parameters for a simple objective function."""
from evolve_core import EvolutionaryAlgorithm, EvolutionConfig, EvolutionStrategy


def objective_function(learning_rate, exploration, temperature):
    """
    A simple test objective: find the combination that maximizes performance.
    In practice, this would be your actual evaluation (model accuracy, etc.)
    """
    # Penalize very high learning rates (instability)
    lr_penalty = max(0, learning_rate - 0.3) * 10

    # Reward exploration balanced with temperature
    score = exploration * temperature - lr_penalty

    # Small noise for realism
    import random
    score += random.gauss(0, 0.01)

    return score


def fitness(chromosome):
    """Wraps the objective function for the evolution engine."""
    return objective_function(
        learning_rate=chromosome.get_value("learning_rate", 0.1),
        exploration=chromosome.get_value("exploration", 0.5),
        temperature=chromosome.get_value("temperature", 1.0),
    )


def define_param_spec():
    """This is the main function that runs the program. It should initialize any required variables and call other functions to handle the actual tasks."""
    # Define paramters to evolve
    gene_specs = [
        {"key": "learning_rate", "min": 0.001, "max": 0.5, "importance": 2.0},
        {"key": "exploration", "min": 0.0, "max": 1.0, "importance": 1.5},
        {"key": "temperature", "min": 0.1, "max": 2.0, "importance": 1.0},
    ]
    return gene_specs

def configure_evolution(config):
    """Configure evolution settings for an AI model."""
    # Configure evolution with adaptive mutation
    EvolutionConfig(
        strategy=EvolutionStrategy.GENETIC_ALGORITHM,
        population_size=30,
        elite_size=3,
        generations=50,
        mutation_rate=0.15,
        crossover_rate=0.7,
        tournament_size=3,
    )


if __name__ == "__main__":
    main()
