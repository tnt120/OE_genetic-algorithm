import time
import logging
from typing import List, Tuple
from numpy.random import random

from config import Config
from real_chromosome import RealChromosome
from real_operators import (
    real_tournament_selection, real_arithmetic_crossover, 
    real_linear_crossover, real_blend_alpha_crossover, real_blend_alpha_beta_crossover,
    real_average_crossover, real_gaussian_mutation, real_uniform_mutation
)


class RealPopulation:
    def __init__(self, config: Config):
        self.config = config
        self.individuals = [
            RealChromosome(self.config)
            for _ in range(self.config.population_size)
        ]

    def evolve(self):
        new_population = []
        if self.config.elitism:
            elite = max(self.individuals, key=lambda x: x.fitness)
            new_population.append(elite)

        while len(new_population) < self.config.population_size:
            winners = self.select()
            
            if random() <= self.config.probability_crossover:
                child1_genes, child2_genes = self.crossover(winners[0], winners[1])
            else:
                child1_genes = winners[0].genes
                child2_genes = winners[1].genes

            # Mutation
            if random() <= self.config.probability_mutation:
                child1_genes = self.mutate(child1_genes)
                child2_genes = self.mutate(child2_genes)

            new_population.append(RealChromosome(config=self.config, genes=child1_genes))
            if len(new_population) < self.config.population_size:
                new_population.append(RealChromosome(config=self.config, genes=child2_genes))

        self.individuals = new_population

    def select(self):
        return real_tournament_selection(self.individuals)
    
    def crossover(self, p1, p2):
        if self.config.crossover_type == "arithmetic":
            return real_arithmetic_crossover(p1, p2)
        elif self.config.crossover_type == "linear":
            return real_linear_crossover(p1, p2)
        elif self.config.crossover_type == "alpha_blend":
            return real_blend_alpha_crossover(p1, p2)
        elif self.config.crossover_type == "alpha_beta_blend":
            return real_blend_alpha_beta_crossover(p1, p2)
        else:
            return real_average_crossover(p1, p2)

    def mutate(self, genes):
        if self.config.mutation_type == "uniform":
            return real_uniform_mutation(RealChromosome(self.config, genes=genes))
        elif self.config.mutation_type == "gaussian":
            return real_gaussian_mutation(RealChromosome(self.config, genes=genes))

    def best(self) -> RealChromosome:
        return max(self.individuals, key=lambda x: x.fitness)

    def __repr__(self):
        return '\n'.join(str(ind) for ind in self.individuals)

    def try_solve(self) -> Tuple[float, RealChromosome, List[dict]]:
        start_time = time.time()
        history = []
        best_in_epoch = None
        
        for epoch in range(self.config.epochs):
            self.evolve()
            best_in_epoch = self.best()
            logging.info(f"Epoch {epoch+1} Best -> {best_in_epoch}")
            
            h = best_in_epoch.to_dict()
            h['epoch_number'] = epoch + 1
            history.append(h)

            if round(best_in_epoch.fitness, 4) == 0.0000:
                logging.info("Found optimal solution")
                break
                
        end_time = time.time()
        if best_in_epoch is None:
            raise ValueError("best chromosome cannot be null")
        elapsed_time = round(end_time - start_time, 2)
        return elapsed_time, best_in_epoch, history 