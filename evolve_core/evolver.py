"""Ability Evolver - High-level evolution orchestration"""
import copy
import json
import hashlib
import time
from typing import Dict, Any, List, Optional, Callable, Tuple

from evolve_core.genome import Chromosome
from evolve_core.evolution import EvolutionConfig, EvolutionStrategy, EvolutionaryAlgorithm
class AbilityEvolver:
    """
    梧桐 ASI 能力进化器
    使用进化算法优化能力参数和策略
    """

    def __init__(self):
        self.ea: Optional[EvolutionaryAlgorithm] = None
        self.ability_params: Dict[str, Any] = {}
        self.evolution_log: List[Dict] = []
        self.stats = {
            "evolutions_run": 0,
            "abilities_improved": set(),
            "generations_completed": 0,
            "best_params_found": {}
        }

from typing import List, Dict

def setup(self, ability_configs: List[Dict]):
    """
    设置进化目标
        
    ability_configs: [
        {"ability": "learning_rate", "min": 0.001, "max": 0.5, "importance": 2.0},
        {"ability": "exploration", "min": 0.0, "max": 1.0, "importance": 1.5},
        ...
    ]
    """
    gene_specs = setup_gene_specs(ability_configs)
    
    # Initialize genetic algorithm
    self.genetic_algorithm.initialize(gene_specs)

def create_gene_spec(cfg: Dict) -> Dict:
    return {
        "key": cfg["ability"],
        "min": cfg["min"],
        "max": cfg["max"],
        "type": cfg.get("type", "parameter"),
        "mutatable": cfg.get("mutatable", True),
        "importance": cfg.get("importance", 1.0)
    }

def setup_gene_specs(ability_configs: List[Dict]) -> List[Dict]:
    """
    设置基因规格

    ability_configs: [
        {"ability": "learning_rate", "min": 0.001, "max": 0.5, "importance": 2.0},
        {"ability": "exploration", "min": 0.0, "max": 1.0, "importance": 1.5},
        ...
    ]
    """
    gene_specs = []
    for cfg in ability_configs:
        gene_specs.append(create_gene_spec(cfg))
    return gene_specs

