from numpy.random import random

from config import POPULATION_SIZE, SELECTION_TYPE, CROSSOVER_TYPE, MUTATION_TYPE, ELITISM, PROBABILITY_MUTATION, PROBABILITY_CROSSOVER, GENES, INVERSION
from chromosome import Chromosome
from selection import tournament_selection, roulette_selection, best_selection
from crossover import single_point_crossover, two_point_crossover, uniform_crossover, grainy_crossover
from mutation import edge_mutation, one_point_mutation, two_point_mutation
from inversion import inverse

class Population:
    def __init__(self):
        # self.individuals = [Chromosome() for _ in range(POPULATION_SIZE)]
        self.individuals = [Chromosome(genes) for genes in GENES]

    def evolve(self):
        new_population = []
        if ELITISM:
            elite = max(self.individuals, key=lambda x: x.fitness)
            new_population.append(elite)

        while len(new_population) < POPULATION_SIZE:
            winners = self.select()
            self.individuals = [ind for ind in self.individuals if ind not in winners]

            if random() <= PROBABILITY_CROSSOVER:
                child1_genes, child2_genes = self.crossover(winners[0], winners[1])
            else:
                child1_genes = winners[0].genes
                child2_genes = winners[1].genes

            if random() <= PROBABILITY_MUTATION:
                child1_genes = self.mutate(child1_genes)
                child2_genes = self.mutate(child2_genes)

            if INVERSION:
                child1_genes = inverse(child1_genes)
                child2_genes = inverse(child2_genes)

            new_population.append(Chromosome(child1_genes))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(Chromosome(child2_genes))

        self.individuals = new_population

    def select(self):
        if SELECTION_TYPE == "tournament":
            return tournament_selection(self.individuals)
        elif SELECTION_TYPE == "roulette":
            return roulette_selection(self.individuals)
        else:
            return best_selection(self.individuals)

    def crossover(self, p1, p2):
        if CROSSOVER_TYPE == "single_point":
            return single_point_crossover(p1, p2)
        elif CROSSOVER_TYPE == "two_point":
            return two_point_crossover(p1, p2)
        elif CROSSOVER_TYPE == "uniform":
            return uniform_crossover(p1, p2)
        else:
            return grainy_crossover(p1, p2)

    def mutate(self, genes):
        if MUTATION_TYPE == "edge":
            return edge_mutation(genes)
        elif MUTATION_TYPE == "one_point":
            return one_point_mutation(genes)
        else:
            return two_point_mutation(genes)

    def best(self):
        return max(self.individuals, key=lambda x: x.fitness)

    def __repr__(self):
        return '\n'.join(str(ind) for ind in self.individuals)