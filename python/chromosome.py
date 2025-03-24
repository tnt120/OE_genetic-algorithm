from config import Config
from utils import binary_to_float, fitness_function
import random


class Chromosome:

    def __init__(self, config: Config, genes=None):
        self.bit_length = config.chromosome_length
        self.dim = config.dimensions
        self.variable_range = config.variable_range
        if genes:
            self.genes = genes
        else:
            self.genes = ''.join(
                random.choice(['0', '1'])
                for _ in range(self.bit_length * self.dim))
        self.fitness = self.evaluate()

    def decode(self):
        return [
            binary_to_float(
                self.genes[i * self.bit_length:(i + 1) * self.bit_length],
                self.variable_range, self.bit_length) for i in range(self.dim)
        ]

    def evaluate(self):
        return fitness_function(self.decode())

    def __repr__(self):
        return f"{self.genes} -> {self.decode()} | fitness: {self.fitness:.4f}"

    def to_dict(self) -> dict:
        x1, x2 = self.decode()
        return {
            "genes": self.genes,
            "x1": x1,
            "x2": x2,
            "fitness": self.fitness
        }
