import random
from config import PROBABILITY_UNIFORM_CROSSOVER

def single_point_crossover(p1, p2):
    point = random.randint(1, len(p1.genes) - 1)
    child1 = p1.genes[:point] + p2.genes[point:]
    child2 = p2.genes[:point] + p1.genes[point:]
    return child1, child2

def two_point_crossover(p1, p2):
    length = len(p1.genes)
    point1 = random.randint(0, length - 2)
    point2 = random.randint(point1 + 1, length - 1)

    child1 = p1.genes[:point1] + p2.genes[point1:point2] + p1.genes[point2:]
    child2 = p2.genes[:point1] + p1.genes[point1:point2] + p2.genes[point2:]
    return child1, child2

def uniform_crossover(p1, p2):
    child1 = ''
    child2 = ''
    for g1, g2 in zip(p1.genes, p2.genes):
        if random.random() < PROBABILITY_UNIFORM_CROSSOVER:
            child1 += g2
            child2 += g1
        else:
            child1 += g1
            child2 += g2
    return child1, child2

def grainy_crossover(p1, p2):
    child = ''
    assert len(p1.genes) == len(p2.genes)
    for i in range(len(p1.genes)):
        a = random.random()
        if a <= 0.5:
            child += p1.genes[i]
        else:
            child += p2.genes[i]
    return child, p2.genes