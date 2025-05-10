import time
import logging
from typing import List, Tuple
from numpy.random import random

from config import Config
from real_chromosome import RealChromosome
from real_operators import (
    real_tournament_selection, real_arithmetic_crossover, 
    real_blend_crossover, real_gaussian_mutation, real_uniform_mutation
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
            # Selection
            parents = real_tournament_selection(self.individuals)
            
            # Crossover
            if random() <= self.config.probability_crossover:
                if self.config.crossover_type == "arithmetic":
                    child1_genes, child2_genes = real_arithmetic_crossover(parents[0], parents[1])
                else:  # blend crossover
                    child1_genes, child2_genes = real_blend_crossover(parents[0], parents[1])
            else:
                child1_genes = parents[0].genes
                child2_genes = parents[1].genes

            # Mutation
            if random() <= self.config.probability_mutation:
                if self.config.mutation_type == "gaussian":
                    child1_genes = real_gaussian_mutation(
                        RealChromosome(self.config, genes=child1_genes))
                    child2_genes = real_gaussian_mutation(
                        RealChromosome(self.config, genes=child2_genes))
                else:  # uniform mutation
                    child1_genes = real_uniform_mutation(
                        RealChromosome(self.config, genes=child1_genes))
                    child2_genes = real_uniform_mutation(
                        RealChromosome(self.config, genes=child2_genes))

            new_population.append(RealChromosome(config=self.config, genes=child1_genes))
            if len(new_population) < self.config.population_size:
                new_population.append(RealChromosome(config=self.config, genes=child2_genes))

        self.individuals = new_population

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