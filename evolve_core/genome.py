"""Genetic algorithm genome - Gene and Chromosome dataclasses"""
import random
import math
import time
import json
import hashlib
import copy
import operator
from typing import Dict, Any, List, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
class GeneType(Enum):
    PARAMETER = "parameter"         # 参数基因
    STRATEGY = "strategy"          # 策略基因
    ARCHITECTURE = "architecture"   # 架构基因
    WEIGHT = "weight"              # 权重基因
    RULE = "rule"                  # 规则基因


class Gene:
    """基因"""
    gene_id: str
    gene_type: GeneType
    key: str
    value: float
    bounds: Tuple[float, float] = (0.0, 1.0)  # 值范围
    mutation_rate: float = 0.1
    crossover_rate: float = 0.7
    importance: float = 1.0  # 对适应度的贡献权重

    def mutate(self, rate: float = None) -> 'Gene':
        """基因突变"""
        rate = rate if rate is not None else self.mutation_rate
        if random.random() < rate:
            delta = random.gauss(0, 0.1) * (self.bounds[1] - self.bounds[0])
            new_val = self.value + delta
            new_val = max(self.bounds[0], min(self.bounds[1], new_val))
            return Gene(
                gene_id=self.gene_id + "_m",
                gene_type=self.gene_type,
                key=self.key,
                value=new_val,
                bounds=self.bounds,
                mutation_rate=self.mutation_rate,
                crossover_rate=self.crossover_rate,
                importance=self.importance
            )
        return copy.deepcopy(self)

    def crossover(self, other: 'Gene') -> Tuple['Gene', 'Gene']:
        """基因交叉"""
        if random.random() < self.crossover_rate and other.gene_type == self.gene_type:
            alpha = random.random()
            v1 = alpha * self.value + (1 - alpha) * other.value
            v2 = (1 - alpha) * self.value + alpha * other.value
            v1 = max(self.bounds[0], min(self.bounds[1], v1))
            v2 = max(self.bounds[0], min(self.bounds[1], v2))
            return (
                Gene(self.gene_id + "_c1", self.gene_type, self.key, v1, self.bounds, self.mutation_rate, self.crossover_rate, self.importance),
                Gene(other.gene_id + "_c2", other.gene_type, other.key, v2, other.bounds, other.mutation_rate, other.crossover_rate, other.importance)
            )
        return copy.deepcopy(self), copy.deepcopy(other)


class Chromosome:
    """染色体 = 一组基因"""
    chromosome_id: str
    genes: List[Gene]
    fitness: float = 0.0
    age: int = 0
    origin: str = "initial"  # initial, crossover, mutation, merge
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def random(cls, gene_specs: List[Dict], origin: str = "initial") -> 'Chromosome':
        """随机创建染色体"""
        cid = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        genes = []
        for spec in gene_specs:
            val = random.uniform(spec["min"], spec["max"])
            genes.append(Gene(
                gene_id=f"{spec['key']}_{cid}",
                gene_type=GeneType(spec.get("type", "parameter")),
                key=spec["key"],
                value=val,
                bounds=(spec["min"], spec["max"]),
                mutation_rate=spec.get("mutation_rate", 0.1),
                crossover_rate=spec.get("crossover_rate", 0.7),
                importance=spec.get("importance", 1.0)
            ))
        return cls(chromosome_id=cid, genes=genes, origin=origin)

    def to_dict(self) -> Dict:
        return {
            "chromosome_id": self.chromosome_id,
            "fitness": self.fitness,
            "age": self.age,
            "origin": self.origin,
            "genes": {g.key: round(g.value, 6) for g in self.genes}
        }

    def get_value(self, key: str, default: float = 0.0) -> float:
        for g in self.genes:
            if g.key == key:
                return g.value
        return default

