import random

def edge_mutation(genes):
    return genes[:-1] + ('1' if genes[-1] == '0' else '0')

def one_point_mutation(genes):
    point = random.randint(0, len(genes) - 1)
    return genes[:point] + ('1' if genes[point] == '0' else '0') +genes[point+1:]

def two_point_mutation(genes):
    length = len(genes)
    point1 = random.randint(0, length - 2)
    point2 = random.randint(point1 + 1, length - 1)
    return genes[:point1] + ('1' if genes[point1] == '0' else '0') + genes[point1+1:point2] + ('1' if genes[point2] == '0' else '0') + genes[point2+1:]