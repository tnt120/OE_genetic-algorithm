from config import Config
from utils import fitness_function
import random


class RealChromosome:
    def __init__(self, config: Config, genes=None):
        self.dim = config.dimensions
        self.variable_range = config.variable_range
        self.config = config
        
        if genes is not None:
            if len(genes) != self.dim:
                raise ValueError(f"Expected {self.dim} genes, got {len(genes)}")
            self.genes = genes
        else:
            self.genes = [
                random.uniform(self.variable_range[0], self.variable_range[1])
                for _ in range(self.dim)
            ]
        
        self.fitness = self.evaluate()

    def evaluate(self):
        return fitness_function(self.genes)

    def __repr__(self):
        return f"{self.genes} | fitness: {self.fitness:.4f}"

    def to_dict(self) -> dict:
        return {
            "genes": self.genes,
            "fitness": self.fitness,
            "points": self.genes,
        }

    def clone(self):
        """Create a copy of the chromosome"""
        return RealChromosome(config=self.config, genes=self.genes.copy()) 