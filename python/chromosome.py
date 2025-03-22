from config import CHROMOSOME_LENGTH, VARIABLE_RANGE, DIMENSIONS
from utils import binary_to_float, fitness_function
import random

class Chromosome:
    def __init__(self, genes=None):
        self.bit_length = CHROMOSOME_LENGTH
        self.dim = DIMENSIONS
        if genes:
            self.genes = genes
        else:
            self.genes = ''.join(random.choice(['0', '1']) for _ in range(self.bit_length * self.dim))
        self.fitness = self.evaluate()

    def decode(self):
        return [binary_to_float(self.genes[i*self.bit_length:(i+1)*self.bit_length], VARIABLE_RANGE, self.bit_length) for i in range(self.dim)]

    def evaluate(self):
        return fitness_function(self.decode())

    def __repr__(self):
        return f"{self.genes} -> {self.decode()} | fitness: {self.fitness:.4f}"
