import random
from chromosome import Chromosome

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


def uniform_crossover(p1, p2, uniform_crossover_proba):
    child1 = ''
    child2 = ''
    for g1, g2 in zip(p1.genes, p2.genes):
        if random.random() < uniform_crossover_proba:
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


def points_to_binary(points, variable_range, bit_length):
    binary = ""
    for point in points:
        point = max(min(point, variable_range[1]), variable_range[0])
        normalized = (point - variable_range[0]) / (variable_range[1] - variable_range[0])
        int_val = int(normalized * (2**bit_length - 1))
        bin_val = format(int_val, f'0{bit_length}b')
        binary += bin_val
    return binary


def arithmetic_crossover(p1, p2):
    alpha = random.random()
    x1 = p1.decode()
    x2 = p2.decode()
    
    child1_points = [alpha * a + (1 - alpha) * b for a, b in zip(x1, x2)]
    child2_points = [(1 - alpha) * a + alpha * b for a, b in zip(x1, x2)]
    
    child1 = points_to_binary(child1_points, p1.variable_range, p1.bit_length)
    child2 = points_to_binary(child2_points, p1.variable_range, p1.bit_length)
    
    return child1, child2


def linear_crossover(p1, p2):
    x1 = p1.decode()
    x2 = p2.decode()
    
    y1 = [0.5 * a + 0.5 * b for a, b in zip(x1, x2)]
    y2 = [1.5 * a - 0.5 * b for a, b in zip(x1, x2)]
    y3 = [-0.5 * a + 1.5 * b for a, b in zip(x1, x2)]
    
    children = [
        points_to_binary(y, p1.variable_range, p1.bit_length)
        for y in [y1, y2, y3]
    ]
    
    fitness_values = [
        Chromosome(p1.config, genes=child).fitness 
        for child in children
    ]
    
    sorted_children = [x for _, x in sorted(zip(fitness_values, children), reverse=True)]
    return sorted_children[0], sorted_children[1]


def alpha_blend_crossover(p1, p2, alpha=0.5):
    x1 = p1.decode()
    x2 = p2.decode()
    
    children = []
    for _ in range(2):
        child_points = []
        for a, b in zip(x1, x2):
            min_val = min(a, b)
            max_val = max(a, b)
            range_val = max_val - min_val
            lower_bound = min_val - alpha * range_val
            upper_bound = max_val + alpha * range_val
            
            child_points.append(random.uniform(lower_bound, upper_bound))
        
        children.append(points_to_binary(child_points, p1.variable_range, p1.bit_length))
    
    return children[0], children[1]


def alpha_beta_blend_crossover(p1, p2, alpha=0.5, beta=0.5):
    x1 = p1.decode()
    x2 = p2.decode()
    
    children = []
    for _ in range(2):
        child_points = []
        for a, b in zip(x1, x2):
            min_val = min(a, b)
            max_val = max(a, b)
            range_val = max_val - min_val
            lower_bound = min_val - alpha * range_val
            upper_bound = max_val + beta * range_val
            
            child_points.append(random.uniform(lower_bound, upper_bound))
        
        children.append(points_to_binary(child_points, p1.variable_range, p1.bit_length))
    
    return children[0], children[1]


def average_crossover(p1, p2):
    x1 = p1.decode()
    x2 = p2.decode()
    
    child_points = [(a + b) / 2 for a, b in zip(x1, x2)]
    child = points_to_binary(child_points, p1.variable_range, p1.bit_length)
    
    return child, child

