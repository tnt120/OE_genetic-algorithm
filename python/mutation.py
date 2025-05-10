import random
from math import exp
from utils import binary_to_float
from chromosome import Chromosome


def edge_mutation(genes):
    pos = random.randint(0, len(genes) - 1)
    return genes[:pos] + ('1' if genes[pos] == '0' else '0') + genes[pos + 1:]


def one_point_mutation(genes):
    pos = random.randint(0, len(genes) - 1)
    return genes[:pos] + ('1' if genes[pos] == '0' else '0') + genes[pos + 1:]


def two_point_mutation(genes):
    pos1 = random.randint(0, len(genes) - 1)
    pos2 = random.randint(0, len(genes) - 1)
    while pos1 == pos2:
        pos2 = random.randint(0, len(genes) - 1)
    genes = list(genes)
    genes[pos1] = '1' if genes[pos1] == '0' else '0'
    genes[pos2] = '1' if genes[pos2] == '0' else '0'
    return ''.join(genes)
