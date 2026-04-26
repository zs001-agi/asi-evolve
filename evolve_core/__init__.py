"""evolve-core: A self-evolving AI framework powered by genetic algorithms.

Provides genetic algorithm primitives (Gene, Chromosome), 
evolution strategies (EvolutionaryAlgorithm), and 
high-level evolution orchestration (AbilityEvolver).
"""

from evolve_core.genome import Gene, GeneType, Chromosome
from evolve_core.evolution import EvolutionConfig, EvolutionStrategy, EvolutionaryAlgorithm
from evolve_core.evolver import AbilityEvolver

__version__ = "0.1.0"
__all__ = [
    "Gene", "GeneType", "Chromosome",
    "EvolutionConfig", "EvolutionStrategy", "EvolutionaryAlgorithm",
    "AbilityEvolver",
]
