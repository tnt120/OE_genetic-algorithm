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


def points_to_binary(points, variable_range, bit_length):
    """
    Convert real values back to binary representation
    """
    binary = ""
    for point in points:
        # Ensure point is within bounds
        point = max(min(point, variable_range[1]), variable_range[0])
        # Normalize the value to [0,1] range
        normalized = (point - variable_range[0]) / (variable_range[1] - variable_range[0])
        # Convert to integer representation
        int_val = int(normalized * (2**bit_length - 1))
        # Convert to binary and pad with zeros
        bin_val = format(int_val, f'0{bit_length}b')
        binary += bin_val
    return binary


def uniform_mutation(chromosome: Chromosome, mutation_range=0.1):
    points = chromosome.decode()
    range_size = chromosome.variable_range[1] - chromosome.variable_range[0]
    delta = mutation_range * range_size
    
    mutated_points = []
    for point in points:
        if random.random() < 1/len(points):  # mutation probability per gene
            mutation = random.uniform(-delta, delta)
            new_value = point + mutation
            # Ensure we stay within bounds
            new_value = max(min(new_value, chromosome.variable_range[1]), 
                          chromosome.variable_range[0])
            mutated_points.append(new_value)
        else:
            mutated_points.append(point)
    
    return points_to_binary(mutated_points, chromosome.variable_range, 
                          chromosome.bit_length)


def gaussian_mutation(chromosome: Chromosome, sigma=0.1):
    points = chromosome.decode()
    range_size = chromosome.variable_range[1] - chromosome.variable_range[0]
    std_dev = sigma * range_size
    
    mutated_points = []
    for point in points:
        if random.random() < 1/len(points):  # mutation probability per gene
            mutation = random.gauss(0, std_dev)
            new_value = point + mutation
            # Ensure we stay within bounds
            new_value = max(min(new_value, chromosome.variable_range[1]), 
                          chromosome.variable_range[0])
            mutated_points.append(new_value)
        else:
            mutated_points.append(point)
    
    return points_to_binary(mutated_points, chromosome.variable_range, 
                          chromosome.bit_length)
