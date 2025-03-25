import random
import numpy as np


def tournament_selection(population, tournament_group_size=4):
    parents = random.choices(population, k=tournament_group_size)
    parents = sorted(parents, key=lambda agent: agent.fitness, reverse=True)
    return parents[0], parents[1]


def roulette_selection(population):
    total_fit = sum(ind.fitness for ind in population)
    rel_fitness = np.array([ind.fitness for ind in population]) / total_fit
    probs = [sum(rel_fitness[:i + 1]) for i in range(len(rel_fitness))]
    selected = []
    for _ in range(2):
        r = random.random()
        for (i, individual) in enumerate(population):
            if r <= probs[i]:
                selected.append(individual)
                break
    return selected


def best_selection(population):
    return sorted(population, key=lambda x: x.fitness, reverse=True)[:2]
