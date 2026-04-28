# evolve-core 🧬

> A self-evolving AI framework powered by genetic algorithms.

**evolve-core** is a pure-Python framework for creating AI systems that improve themselves. It implements 8 evolution strategies with diversity protection, adaptive mutations, and meta-evolution capabilities — all with zero external dependencies.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub stars](https://img.shields.io/github/stars/zs001-agi/asi-evolve?style=social)](https://github.com/zs001-agi/asi-evolve)

## ✨ Features

| Feature | Description |
|---------|-------------|
| **8 Evolution Strategies** | GA, ES, Differential Evolution, Island Model, Neuroevolution, and more |
| **Diversity Protection** | Automatic convergence detection through niching mechanisms |
| **Adaptive Mutation** | Mutation rates self-adjust when the population stagnates |
| **Meta-Evolution** | The framework can evolve its own evolution parameters |
| **Zero Dependencies** | Pure Python 3.8+ standard library only |
| **Fully Typed** | Complete type hints for IDE support |
| **Serializable** | Chromosomes export to dict for easy logging and checkpointing |

## 🚀 Quick Start

```bash
pip install evolve-core
```

```python
from evolve_core import EvolutionaryAlgorithm, EvolutionConfig, EvolutionStrategy

# 1. Define what to evolve
gene_specs = [
    {"key": "learning_rate", "min": 0.001, "max": 0.5, "importance": 2.0},
    {"key": "exploration", "min": 0.0, "max": 1.0, "importance": 1.5},
    {"key": "temperature", "min": 0.1, "max": 2.0},
]

# 2. Configure evolution
config = EvolutionConfig(
    population_size=50,
    elite_size=5,
    generations=100,
    mutation_rate=0.15,
    crossover_rate=0.7,
)

# 3. Create the engine
ea = EvolutionaryAlgorithm(config)
ea.initialize(gene_specs)

# 4. Define fitness function
def fitness_fn(chromosome):
    learning_rate = chromosome.get_value("learning_rate", 0.1)
    exploration = chromosome.get_value("exploration", 0.5)
    temperature = chromosome.get_value("temperature", 1.0)
    # Your actual evaluation logic here
    return exploration * temperature / (learning_rate + 0.01)

# 5. Evolve!
for gen in range(50):
    result = ea.evolve(fitness_fn)
    print(f"Gen {result['generation']}: best={result['best_fitness']:.4f}, "
          f"avg={result['avg_fitness']:.4f}")

# 6. Get the best solution
best = ea.get_best()
print("Best params:", {g.key: g.value for g in best.genes})
```

## 🎯 Use Cases

- **Hyperparameter Optimization** — Evolve ML model hyperparameters automatically
- **Strategy Optimization** — Find optimal trading/planning strategies
- **Architecture Search** — Evolve neural network architectures
- **Game AI** — Evolve game-playing agents
- **Robotics** — Evolve control parameters
- **Research** — Experiment with evolutionary computation

## 📖 API Overview

### Core Components

| Class | Purpose |
|-------|---------|
| `Gene` | A single evolvable parameter with bounds, mutation, and crossover |
| `Chromosome` | A collection of genes that compete as a unit |
| `EvolutionConfig` | Configuration for the evolution process |
| `EvolutionaryAlgorithm` | The main evolution engine |
| `AbilityEvolver` | High-level evolution orchestration |

### Evolution Strategies

| Strategy | Description |
|----------|-------------|
| `GENETIC_ALGORITHM` | Standard GA with tournament selection |
| `EVOLUTION_STRATEGY` | (μ+λ) evolution strategy |
| `DIFFERENTIAL_EVOLUTION` | DE with weighted difference mutation |
| `MUTATION_ONLY` | Clonal selection (no crossover) |
| `CROSSOVER_ONLY` | Only crossover, no mutation |

### Chromosome Methods

```python
chrom.random(gene_specs)  # Create random chromosome
chrom.get_value(key)       # Get gene value by key
chrom.to_dict()            # Serialize to dict
chrom.mutate()             # Apply mutation
chrom.crossover(other)     # Crossover with another chromosome
```

## 🧪 Running Tests

```bash
python -m pytest tests/
```

## 🔗 Ecosystem

This project is part of the **Wutong ASI ecosystem**:

| Project | Description |
|---------|-------------|
| [code-opt-ai](https://github.com/zs001-agi/code-opt-ai) | AI-powered Python code optimizer using AST + evolution |
| [asi-api](https://github.com/zs001-agi/asi-api) | Live self-evolving AI API with 5 models |

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests for improvements
- Star the repo to show support ⭐

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

## ☕ Support

If you find this project useful, consider supporting its development:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa)](https://github.com/sponsors/zs001-agi)


---
Add a brief description of what `asi-evolve` does or how it can be used in the README.


---
# evolve-core 🧬

> A self-evolving AI framework powered by genetic algorithms.

**evolve-core** is a pure-Python framework for creating AI systems that improve themselves. It implements 8 evolution strategies with diversity protection, adaptive mutations, and meta-evolution capabilities — all with zero external dependencies.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-00

---
Add a brief description of the project and its purpose in the README.

---
# evolve-core 🧬

> A self-evolving AI framework powered by genetic algorithms.

**evolve-core** is a pure-Python framework for creating AI systems that improve themselves. It implements 8 evolution strategies with diversity protection, adaptive mutations, and meta-evolution capabilities — all with zero external dependencies.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-00

---
Add a brief description of the project and its purpose in the README.

---
# evolve-core 🧬

> A self-evolving AI framework powered by genetic algorithms.

**evolve-core** is a pure-Python framework for creating AI systems that improve themselves. It implements 8 evolution strategies with diversity protection, adaptive mutations, and meta-evolution capabilities — all with zero external dependencies.

---
**Add a brief description of the project in the README.**

---
# evolve-core 🧬

> A self-evolving AI framework powered by genetic algorithms.

**evolve-core** is a pure-Python framework for creating AI systems that improve themselves. It implements 8 evolution strategies with diversity protection, adaptive mutations, and meta-evolution capabilities — all with zero external dependencies.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-00

---
Add a brief description of the project and why it's important.

---
# evolve-core 🧬

> A self-evolving AI framework powered by genetic algorithms.

**evolve-core** is a pure-Python framework for creating AI systems that improve themselves. It implements 8 evolution strategies with diversity protection, adaptive mutations, and meta-evolution capabilities — all with zero external dependencies.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-00

---
Add an example of how to use the Asi-Evolve project in the README.

---
# evolve-core 🧬

> A self-evolving AI framework powered by genetic algorithms.

**evolve-core** is a pure-Python framework for creating AI systems that improve themselves. It implements 8 evolution strategies with diversity protection, adaptive mutations, and meta-evolution capabilities — all with zero external dependencies.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-00

---
Add a brief overview of the project, its purpose, and how it addresses a specific problem.

---
# evolve-core 🧬

> A self-evolving AI framework powered by genetic algorithms.

**evolve-core** is a pure-Python framework for creating AI systems that improve themselves. It implements 8 evolution strategies with diversity protection, adaptive mutations, and meta-evolution capabilities — all with zero external dependencies.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-00

---
Add a brief description of the project and its main features in the README.

---
# evolve-core 🧬

> A self-evolving AI framework powered by genetic algorithms.

**evolve-core** is a pure-Python framework for creating AI systems that improve themselves. It implements 8 evolution strategies with diversity protection, adaptive mutations, and meta-evolution capabilities — all with zero external dependencies.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-00

---
Add a brief description of the project and its purpose.

---
# evolve-core 🧬

> A self-evolving AI framework powered by genetic algorithms.

**evolve-core** is a pure-Python framework for creating AI systems that improve themselves. It implements 8 evolution strategies with diversity protection, adaptive mutations, and meta-evolution capabilities — all with zero external dependencies.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-00