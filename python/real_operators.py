import random
from typing import List, Tuple
from real_chromosome import RealChromosome


def real_tournament_selection(population: List[RealChromosome], tournament_size: int = 2) -> List[RealChromosome]:
    """Tournament selection for real-valued chromosomes"""
    tournament = random.sample(population, tournament_size)
    winner1 = max(tournament, key=lambda x: x.fitness)
    
    # Select second parent
    tournament = random.sample(population, tournament_size)
    winner2 = max(tournament, key=lambda x: x.fitness)
    
    return [winner1, winner2]


def real_arithmetic_crossover(p1: RealChromosome, p2: RealChromosome) -> Tuple[List[float], List[float]]:
    """Arithmetic crossover for real-valued chromosomes"""
    alpha = random.random()
    child1_genes = [alpha * g1 + (1 - alpha) * g2 for g1, g2 in zip(p1.genes, p2.genes)]
    child2_genes = [(1 - alpha) * g1 + alpha * g2 for g1, g2 in zip(p1.genes, p2.genes)]
    return child1_genes, child2_genes

def real_linear_crossover(p1: RealChromosome, p2: RealChromosome) -> Tuple[List[float], List[float]]:
    """Linear crossover for real-valued chromosomes"""
    y1 = [0.5 * a + 0.5 * b for a, b in zip(p1.genes, p2.genes)]
    y2 = [1.5 * a - 0.5 * b for a, b in zip(p1.genes, p2.genes)]
    y3 = [-0.5 * a + 1.5 * b for a, b in zip(p1.genes, p2.genes)]

    candidates = [y1, y2, y3]
    chromosomes = [RealChromosome(p1.config, genes=c) for c in candidates]
    chromosomes.sort(key=lambda x: x.fitness, reverse=True)
    
    return chromosomes[0].genes, chromosomes[1].genes

def real_blend_alpha_crossover(p1: RealChromosome, p2: RealChromosome, alpha: float = 0.5) -> Tuple[List[float], List[float]]:
    """BLX-α crossover for real-valued chromosomes"""
    child1_genes = []
    child2_genes = []
    
    for g1, g2 in zip(p1.genes, p2.genes):
        min_val = min(g1, g2)
        max_val = max(g1, g2)
        range_val = max_val - min_val
        
        lower_bound = max(min_val - alpha * range_val, p1.variable_range[0])
        upper_bound = min(max_val + alpha * range_val, p1.variable_range[1])
        
        child1_genes.append(random.uniform(lower_bound, upper_bound))
        child2_genes.append(random.uniform(lower_bound, upper_bound))
    
    return child1_genes, child2_genes

def real_blend_alpha_beta_crossover(p1: RealChromosome, p2: RealChromosome, alpha: float = 0.3, beta: float = 0.5) -> Tuple[List[float], List[float]]:
    """BLX-αβ crossover for real-valued chromosomes"""
    child1_genes = []
    child2_genes = []

    for g1, g2 in zip(p1.genes, p2.genes):
        min_val = min(g1, g2)
        max_val = max(g1, g2)
        d = max_val - min_val

        lower = max(min_val - alpha * d, p1.variable_range[0])
        upper = min(max_val + beta * d, p1.variable_range[1])

        child1_genes.append(random.uniform(lower, upper))
        child2_genes.append(random.uniform(lower, upper))

    return child1_genes, child2_genes

def real_average_crossover(p1: RealChromosome, p2: RealChromosome) -> Tuple[List[float], List[float]]:
    """Average crossover for real-valued chromosomes"""
    avg = [(a + b) / 2 for a, b in zip(p1.genes, p2.genes)]
    return avg, avg


def real_gaussian_mutation(chromosome: RealChromosome, sigma: float = 0.1) -> List[float]:
    """Gaussian mutation for real-valued chromosomes"""
    range_size = chromosome.variable_range[1] - chromosome.variable_range[0]
    std_dev = sigma * range_size
    
    mutated_genes = []
    for gene in chromosome.genes:
        if random.random() < 1/len(chromosome.genes):
            mutation = random.gauss(0, std_dev)
            new_value = gene + mutation
            new_value = max(min(new_value, chromosome.variable_range[1]), 
                          chromosome.variable_range[0])
            mutated_genes.append(new_value)
        else:
            mutated_genes.append(gene)
    
    return mutated_genes


def real_uniform_mutation(chromosome: RealChromosome, mutation_range: float = 0.1) -> List[float]:
    """Uniform mutation for real-valued chromosomes"""
    range_size = chromosome.variable_range[1] - chromosome.variable_range[0]
    delta = mutation_range * range_size
    
    mutated_genes = []
    for gene in chromosome.genes:
        if random.random() < 1/len(chromosome.genes):
            mutation = random.uniform(-delta, delta)
            new_value = gene + mutation
            new_value = max(min(new_value, chromosome.variable_range[1]), 
                          chromosome.variable_range[0])
            mutated_genes.append(new_value)
        else:
            mutated_genes.append(gene)
    
    return mutated_genes 