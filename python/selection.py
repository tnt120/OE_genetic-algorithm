import random
import numpy as np

def tournament_selection(population, tournament_size=4, num_tournaments=4):
    shuffled = random.sample(population, len(population))
    tournament_winners = []

    for i in range(num_tournaments):
        group = shuffled[i * tournament_size : (i + 1) * tournament_size]
        winner = max(group, key=lambda x: x.fitness)
        tournament_winners.append(winner)

    top_two = sorted(tournament_winners, key=lambda x: x.fitness, reverse=True)[:2]
    return top_two

def roulette_selection(population):
    total_fit = sum(ind.fitness for ind in population)
    rel_fitness = np.array([ind.fitness for ind in population]) / total_fit
    probs = [sum(rel_fitness[:i + 1]) for i in range(len(rel_fitness))]
    selected = []
    for n in range(2):
        r = random.random()
        for (i, individual) in enumerate(population):
            if r <= probs[i]:
                selected.append(individual)
                break
    return selected

def best_selection(population):
    return sorted(population, key=lambda x: x.fitness, reverse=True)[:2]