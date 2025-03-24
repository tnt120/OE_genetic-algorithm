import time
import logging
from typing import List, Tuple
from numpy.random import random

from config import Config, GENES
from chromosome import Chromosome
from selection import tournament_selection, roulette_selection, best_selection
from crossover import single_point_crossover, two_point_crossover, uniform_crossover, grainy_crossover
from mutation import edge_mutation, one_point_mutation, two_point_mutation
from inversion import inverse


class Population:

    def __init__(self, config: Config, use_default: bool = True):
        self.config = config
        if use_default:
            self.individuals = [
                Chromosome(config=self.config, genes=gen) for gen in GENES
            ]
        else:
            self.individuals = [
                Chromosome(self.config)
                for _ in range(self.config.population_size)
            ]

    def evolve(self):
        new_population = []
        if self.config.elitism:
            elite = max(self.individuals, key=lambda x: x.fitness)
            new_population.append(elite)

        while len(new_population) < self.config.population_size:
            winners = self.select()
            self.individuals = [
                ind for ind in self.individuals if ind not in winners
            ]

            if random() <= self.config.probability_crossover:
                child1_genes, child2_genes = self.crossover(
                    winners[0], winners[1])
            else:
                child1_genes = winners[0].genes
                child2_genes = winners[1].genes

            if random() <= self.config.probability_mutation:
                child1_genes = self.mutate(child1_genes)
                child2_genes = self.mutate(child2_genes)

            if self.config.inversion:
                child1_genes = inverse(child1_genes)
                child2_genes = inverse(child2_genes)

            new_population.append(
                Chromosome(config=self.config, genes=child1_genes))
            if len(new_population) < self.config.population_size:
                new_population.append(
                    Chromosome(config=self.config, genes=child2_genes))

        self.individuals = new_population

    def select(self):
        if self.config.selection_type == "tournament":
            return tournament_selection(self.individuals)
        elif self.config.selection_type == "roulette":
            return roulette_selection(self.individuals)
        else:
            return best_selection(self.individuals)

    def crossover(self, p1, p2):
        if self.config.crossover_type == "single_point":
            return single_point_crossover(p1, p2)
        elif self.config.crossover_type == "two_point":
            return two_point_crossover(p1, p2)
        elif self.config.crossover_type == "uniform":
            return uniform_crossover(p1, p2,
                                     self.config.probability_uniform_crossover)
        else:
            return grainy_crossover(p1, p2)

    def mutate(self, genes):
        if self.config.mutation_type == "edge":
            return edge_mutation(genes)
        elif self.config.mutation_type == "one_point":
            return one_point_mutation(genes)
        else:
            return two_point_mutation(genes)

    def best(self) -> Chromosome:
        return max(self.individuals, key=lambda x: x.fitness)

    def __repr__(self):
        return '\n'.join(str(ind) for ind in self.individuals)

    def try_solve(self) -> Tuple[float, Chromosome, List[dict]]:
        start_time = time.time()
        history = []
        best_in_epoch = None
        for epoch in range(self.config.epochs):
            self.evolve()
            best_in_epoch = self.best()
            logging.info(f"Epoka {epoch+1} Najlepszy -> {best_in_epoch}")
            history.append(best_in_epoch.to_dict())

            if round(best_in_epoch.fitness, 4) == 0.0000:
                logging.info("Znalezione optymalne rozwiązanie")
                break
        end_time = time.time()
        if best_in_epoch is None:
            raise ValueError("best chromosome cannot be null")
        elapsed_time = round(end_time - start_time, 2)
        return elapsed_time, best_in_epoch, history
