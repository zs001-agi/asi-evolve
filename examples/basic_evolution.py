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


def main():
    # 1. Define paramters to evolve
    gene_specs = [
        {"key": "learning_rate", "min": 0.001, "max": 0.5, "importance": 2.0},
        {"key": "exploration", "min": 0.0, "max": 1.0, "importance": 1.5},
        {"key": "temperature", "min": 0.1, "max": 2.0, "importance": 1.0},
    ]

    # 2. Configure evolution with adaptive mutation
    config = EvolutionConfig(
        strategy=EvolutionStrategy.GENETIC_ALGORITHM,
        population_size=30,
        elite_size=3,
        generations=50,
        mutation_rate=0.15,
        crossover_rate=0.7,
        tournament_size=3,
        adapt_mutation=True,  # Auto-increase mutation when stuck
    )

    # 3. Initialize
    ea = EvolutionaryAlgorithm(config)
    ea.initialize(gene_specs)

    print(f"Starting evolution with {config.population_size} individuals...")
    print(f"{'Gen':>4} {'Best':>8} {'Avg':>8} {'Div':>6} {'Top Params'}")
    print("-" * 60)

    # 4. Run evolution
    for gen in range(config.generations):
        result = ea.evolve(fitness)

        if gen % 10 == 0 or gen == config.generations - 1:
            best = ea.get_best()
            params = {g.key: f"{g.value:.4f}" for g in best.genes}
            print(f"{result['generation']:>4d} {result['best_fitness']:>8.4f} "
                  f"{result['avg_fitness']:>8.4f} {result['diversity']:>6.4f} "
                  f"{dict(params)}")

    # 5. Results
    print("\n" + "=" * 60)
    print("EVOLUTION COMPLETE!")
    print(f"Generations: {ea.generation}")
    print(f"Best fitness ever: {ea.stats['best_fitness_ever']:.4f}")
    best = ea.get_best()
    if best:
        print(f"Best parameters: {best.to_dict()}")
        print(f"Best origin: {best.origin}")
    print("=" * 60)


if __name__ == "__main__":
    main()
