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

    def setup(self, ability_configs: List[Dict]):
        """
        设置进化目标
        
        ability_configs: [
            {"ability": "learning_rate", "min": 0.001, "max": 0.5, "importance": 2.0},
            {"ability": "exploration", "min": 0.0, "max": 1.0, "importance": 1.5},
            ...
        ]
        """
        gene_specs = []
        for cfg in ability_configs:
            gene_specs.append({
                "key": cfg["ability"],
                "min": cfg["min"],
                "max": cfg["max"],
                "type": cfg.get("type", "parameter"),
                "mutation_rate": cfg.get("mutation_rate", 0.1),
                "crossover_rate": cfg.get("crossover_rate", 0.7),
                "importance": cfg.get("importance", 1.0)
            })
        
        config = EvolutionConfig(
            strategy=EvolutionStrategy.GENETIC_ALGORITHM,
            population_size=30,
            elite_size=3,
            generations=50,
            tournament_size=5
        )
        
        self.ea = EvolutionaryAlgorithm(config)
        self.ea.initialize(gene_specs)
        self.ability_params = {cfg["ability"]: cfg for cfg in ability_configs}

    def fitness_fn(self, chrom: Chromosome) -> float:
        """
        适应度函数
        这里需要根据实际能力表现计算适应度
        子类应该覆盖此方法
        """
        # 默认适应度：基因值的加权和（越高越好）
        score = 0.0
        for gene in chrom.genes:
            # 归一化值
            norm_val = (gene.value - gene.bounds[0]) / max(gene.bounds[1] - gene.bounds[0], 0.001)
            score += norm_val * gene.importance
        
        # 惩罚多样性过低
        diversity = self.ea._calculate_diversity() if self.ea else 0
        if diversity < 0.1:
            score *= 0.5
        
        return score

    def evolve_generations(self, n: int = 10, verbose: bool = True) -> Dict[str, Any]:
        """运行 n 代进化"""
        if self.ea is None:
            return {"error": "Not initialized. Call setup() first."}
        
        results = []
        for i in range(n):
            result = self.ea.evolve(self.fitness_fn)
            results.append(result)
            self.stats["generations_completed"] += 1
            
            if verbose and i % 5 == 0:
                print(f"Gen {result['generation']}: best={result['best_fitness']:.4f}, "
                      f"avg={result['avg_fitness']:.4f}, div={result['diversity']:.4f}")
        
        self.stats["evolutions_run"] += 1
        
        # 更新最佳参数
        best = self.ea.get_best()
        if best:
            self.stats["best_params_found"] = best.to_dict()
            for gene in best.genes:
                self.stats["abilities_improved"].add(gene.key)
        
        return {
            "generations": results,
            "best": self.ea.get_report(),
            "stats": {**self.stats, "abilities_improved": list(self.stats["abilities_improved"])}
        }

    def get_best_params(self) -> Dict[str, float]:
        """获取最佳参数"""
        best = self.ea.get_best() if self.ea else None
        if not best:
            return {}
        return {g.key: g.value for g in best.genes}

    def get_report(self) -> Dict[str, Any]:
        return {
            "evolver_stats": {**self.stats, "abilities_improved": list(self.stats["abilities_improved"])},
            "ea_report": self.ea.get_report() if self.ea else {"status": "not_initialized"}
        }

