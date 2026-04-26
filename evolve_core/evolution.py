"""Evolutionary algorithm engine - multiple evolution strategies"""
import random, math, time, json, hashlib, copy
from typing import Dict, Any, List, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from evolve_core.genome import GeneType, Gene, Chromosome

class EvolutionStrategy(Enum):
    GENETIC_ALGORITHM = "ga"          # 标准遗传算法
    EVOLUTION_STRATEGY = "es"        # 进化策略 (1+1, μ+λ)
    DIFFERENTIAL_EVOLUTION = "de"      # 差分进化
    MODEL_MERGE = "model_merge"       # 模型融合
    CROSSOVER_ONLY = "crossover_only" # 仅交叉
    MUTATION_ONLY = "mutation_only"   # 仅突变
    ISLAND_MODEL = "island"          # 岛屿模型
    NEUROEVOLUTION = "neuro"         # 神经进化

@dataclass
class EvolutionConfig:
    """进化配置"""
    strategy: EvolutionStrategy = EvolutionStrategy.GENETIC_ALGORITHM
    population_size: int = 50
    elite_size: int = 5
    generations: int = 100
    mutation_rate: float = 0.15
    crossover_rate: float = 0.7
    tournament_size: int = 3
    # ES specific
    offspring_count: int = 10  # μ+λ 中的 λ
    parent_count: int = 5     # μ+λ 中的 μ
    # 模型融合
    merge_methods: List[str] = field(default_factory=lambda: ["dare", "task_arithmetic", "ties"])
    # 多样性
    diversity_threshold: float = 0.1
    niching: bool = True
    # 元进化
    meta_learning: bool = True
    adapt_mutation: bool = True
    adapt_crossover: bool = True

class EvolutionaryAlgorithm:
    """
    进化算法引擎
    支持多种进化策略：GA, ES, DE, 模型融合
    """

    def __init__(self, config: EvolutionConfig = None):
        self.config = config or EvolutionConfig()
        self.population: List[Chromosome] = []
        self.best_chromosome: Optional[Chromosome] = None
        self.history: List[Dict] = []
        self.generation: int = 0
        self.stats = {
            "total_evaluations": 0,
            "total_mutations": 0,
            "total_crossovers": 0,
            "total_merges": 0,
            "best_fitness_ever": 0.0,
            "stagnation_count": 0,
            "diversity_history": []
        }

    def initialize(self, gene_specs: List[Dict]):
        """初始化种群"""
        self.population = [
            Chromosome.random(gene_specs, origin="initial")
            for _ in range(self.config.population_size)
        ]
        self.generation = 0
        self.best_chromosome = None

    def evaluate_population(self, fitness_fn: Callable[[Chromosome], float]):
        """评估种群"""
        for chrom in self.population:
            if chrom.fitness == 0:  # 未评估
                chrom.fitness = fitness_fn(chrom)
                self.stats["total_evaluations"] += 1
        
        # 更新最佳
        current_best = max(self.population, key=lambda c: c.fitness)
        if self.best_chromosome is None or current_best.fitness > self.best_chromosome.fitness:
            self.best_chromosome = copy.deepcopy(current_best)
            self.stats["stagnation_count"] = 0
        else:
            self.stats["stagnation_count"] += 1
        
        self.stats["best_fitness_ever"] = max(
            self.stats["best_fitness_ever"],
            current_best.fitness
        )

    def evolve(self, fitness_fn: Callable[[Chromosome], float]) -> Dict[str, Any]:
        """
        执行一代进化
        返回: 进化统计
        """
        self.generation += 1
        self.evaluate_population(fitness_fn)
        
        # 多样性检查
        diversity = self._calculate_diversity()
        self.stats["diversity_history"].append(diversity)
        
        # 选择
        selected = self._select()
        
        # 繁殖
        new_population = self._reproduce(selected)
        
        # 更新
        self.population = new_population
        
        # 记录历史
        best = max(self.population, key=lambda c: c.fitness)
        avg = sum(c.fitness for c in self.population) / len(self.population)
        
        history_entry = {
            "generation": self.generation,
            "best_fitness": best.fitness,
            "avg_fitness": avg,
            "diversity": diversity,
            "stagnation": self.stats["stagnation_count"],
            "best_origin": best.origin
        }
        self.history.append(history_entry)
        
        return history_entry

    def _calculate_diversity(self) -> float:
        """计算种群多样性（基因距离标准差）"""
        if not self.population:
            return 0.0
        if len(self.population) < 2:
            return 0.0
        
        # 使用最相似染色体的平均距离作为多样性度量
        total_distance = 0.0
        count = 0
        for i, c1 in enumerate(self.population):
            for c2 in self.population[i+1:]:
                dist = self._chromosome_distance(c1, c2)
                total_distance += dist
                count += 1
        
        return total_distance / max(count, 1)

    def _chromosome_distance(self, c1: Chromosome, c2: Chromosome) -> float:
        """计算两个染色体的距离"""
        genes1 = {g.key: g.value for g in c1.genes}
        genes2 = {g.key: g.value for g in c2.genes}
        
        all_keys = set(genes1.keys()) | set(genes2.keys())
        if not all_keys:
            return 0.0
        
        total = 0.0
        for key in all_keys:
            v1 = genes1.get(key, 0)
            v2 = genes2.get(key, 0)
            total += (v1 - v2) ** 2
        
        return math.sqrt(total / len(all_keys))

    def _select(self) -> List[Chromosome]:
        """选择"""
        strategy = self.config.strategy
        
        if strategy == EvolutionStrategy.GENETIC_ALGORITHM:
            return self._tournament_select()
        elif strategy == EvolutionStrategy.EVOLUTION_STRATEGY:
            return self._es_select()
        elif strategy == EvolutionStrategy.CROSSOVER_ONLY:
            return self._fitness_proportional_select()
        else:
            return self._tournament_select()

    def _tournament_select(self) -> List[Chromosome]:
        """锦标赛选择"""
        k = min(self.config.tournament_size, len(self.population))
        selected = []
        for _ in range(len(self.population)):
            contestants = random.sample(self.population, k)
            winner = max(contestants, key=lambda c: c.fitness)
            selected.append(copy.deepcopy(winner))
        return selected

    def _es_select(self) -> List[Chromosome]:
        """进化策略选择 (μ+λ)"""
        parents = sorted(self.population, key=lambda c: c.fitness, reverse=True)[:self.config.parent_count]
        return parents

    def _fitness_proportional_select(self) -> List[Chromosome]:
        """适应度比例选择"""
        total = sum(max(c.fitness, 0.01) for c in self.population)
        selected = []
        for _ in range(len(self.population)):
            r = random.random() * total
            cum = 0
            for c in self.population:
                cum += max(c.fitness, 0.01)
                if cum >= r:
                    selected.append(copy.deepcopy(c))
                    break
        return selected

    def _reproduce(self, selected: List[Chromosome]) -> List[Chromosome]:
        """繁殖"""
        strategy = self.config.strategy
        new_pop = []
        
        # 精英保留
        elite = sorted(self.population, key=lambda c: c.fitness, reverse=True)[:self.config.elite_size]
        new_pop.extend(copy.deepcopy(e) for e in elite)
        
        if strategy == EvolutionStrategy.GENETIC_ALGORITHM:
            new_pop.extend(self._ga_reproduce(selected))
        elif strategy == EvolutionStrategy.EVOLUTION_STRATEGY:
            new_pop.extend(self._es_reproduce(selected))
        elif strategy == EvolutionStrategy.DIFFERENTIAL_EVOLUTION:
            new_pop.extend(self._de_reproduce(selected))
        elif strategy == EvolutionStrategy.MUTATION_ONLY:
            new_pop.extend(self._mutation_only_reproduce(selected))
        else:
            new_pop.extend(self._ga_reproduce(selected))
        
        # 填充到种群大小
        while len(new_pop) < self.config.population_size:
            new_pop.append(copy.deepcopy(random.choice(self.population)))
        
        return new_pop[:self.config.population_size]

    def _ga_reproduce(self, selected: List[Chromosome]) -> List[Chromosome]:
        """GA繁殖：交叉+突变"""
        children = []
        while len(children) < self.config.population_size - self.config.elite_size:
            p1, p2 = random.sample(selected, 2)
            c1, c2 = self._crossover(p1, p2)
            c1 = self._mutate(c1)
            c2 = self._mutate(c2)
            c1.origin = "crossover"
            c2.origin = "crossover"
            children.extend([c1, c2])
        return children[:self.config.population_size - self.config.elite_size]

    def _es_reproduce(self, parents: List[Chromosome]) -> List[Chromosome]:
        """进化策略繁殖 (μ+λ)"""
        children = []
        for _ in range(self.config.offspring_count):
            p = random.choice(parents)
            child = self._mutate(copy.deepcopy(p))
            child.origin = "mutation"
            child.age = 0
            children.append(child)
        return children

    def _de_reproduce(self, selected: List[Chromosome]) -> List[Chromosome]:
        """差分进化"""
        children = []
        F = 0.5  # 差分权重
        CR = 0.7  # 交叉概率
        
        for i in range(len(selected)):
            a, b, c = random.sample(selected, 3)
            trial = copy.deepcopy(a)
            
            for j, gene in enumerate(trial.genes):
                if random.random() < CR:
                    diff = b.genes[j].value - c.genes[j].value
                    trial.genes[j].value = a.genes[j].value + F * diff
                    trial.genes[j].value = max(
                        trial.genes[j].bounds[0],
                        min(trial.genes[j].bounds[1], trial.genes[j].value)
                    )
            
            trial.origin = "de"
            children.append(trial)
        
        return children[:self.config.population_size - self.config.elite_size]

    def _mutation_only_reproduce(self, selected: List[Chromosome]) -> List[Chromosome]:
        """仅突变繁殖"""
        children = []
        for p in selected:
            child = self._mutate(copy.deepcopy(p))
            child.origin = "mutation"
            children.append(child)
        return children[:self.config.population_size - self.config.elite_size]

    def _crossover(self, p1: Chromosome, p2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        """染色体交叉"""
        g1_map = {g.key: g for g in p1.genes}
        g2_map = {g.key: g for g in p2.genes}
        all_keys = list(g1_map.keys())
        
        # 均匀交叉
        new_genes1, new_genes2 = [], []
        for key in all_keys:
            g1, g2 = g1_map[key], g2_map[key]
            c1g, c2g = g1.crossover(g2)
            new_genes1.append(c1g)
            new_genes2.append(c2g)
        
        cid1 = hashlib.md5(f"{p1.chromosome_id}{time.time()}".encode()).hexdigest()[:8]
        cid2 = hashlib.md5(f"{p2.chromosome_id}{time.time()}".encode()).hexdigest()[:8]
        
        c1 = Chromosome(chromosome_id=cid1, genes=new_genes1, origin="crossover")
        c2 = Chromosome(chromosome_id=cid2, genes=new_genes2, origin="crossover")
        
        self.stats["total_crossovers"] += 1
        return c1, c2

    def _mutate(self, chrom: Chromosome) -> Chromosome:
        """染色体突变"""
        new_genes = []
        for gene in chrom.genes:
            # 自适应突变率
            rate = gene.mutation_rate
            if self.config.adapt_mutation and self.stats["stagnation_count"] > 5:
                rate *= 2.0  # 停滞时增加突变
            
            new_gene = gene.mutate(rate)
            if new_gene is not gene:  # 发生了突变
                self.stats["total_mutations"] += 1
                new_genes.append(new_gene)
            else:
                new_genes.append(gene)
        
        chrom.genes = new_genes
        chrom.age += 1
        return chrom

    def get_best(self) -> Optional[Chromosome]:
        """获取最佳染色体"""
        return self.best_chromosome

    def get_report(self) -> Dict[str, Any]:
        """获取进化报告"""
        if not self.history:
            return {"status": "not_started"}
        
        recent = self.history[-10:]
        best_in_recent = max(h["best_fitness"] for h in recent)
        diversity_trend = recent[-1]["diversity"] - recent[0]["diversity"]
        
        return {
            "generation": self.generation,
            "total_evaluations": self.stats["total_evaluations"],
            "best_fitness_ever": self.stats["best_fitness_ever"],
            "current_best": self.history[-1]["best_fitness"] if self.history else 0,
            "avg_fitness": self.history[-1]["avg_fitness"] if self.history else 0,
            "diversity": self.history[-1]["diversity"] if self.history else 0,
            "diversity_trend": diversity_trend,
            "stagnation": self.stats["stagnation_count"],
            "strategy": self.config.strategy.value,
            "population_size": len(self.population),
            "best_chromosome": self.best_chromosome.to_dict() if self.best_chromosome else None,
            "recent_history": recent
        }