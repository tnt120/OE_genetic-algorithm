import random


def inverse(genes):
    point1 = random.randint(0, len(genes) - 2)
    point2 = random.randint(point1 + 1, len(genes) - 1)
    return genes[:point1] + genes[point1:point2][::-1] + genes[point2:]
