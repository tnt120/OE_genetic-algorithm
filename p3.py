#na podstawie przykładu: https://pypi.org/project/pygad/1.0.18/

import pygad
import matplotlib.pyplot as plt
import benchmark_functions as bf
from utils import get_logger, decode_binary_solution, plot_custom_fitness, plot_compare_fitness
from stats_collector import GenerationStatsCollector

import os
from config import Config


def real_gad(config, func, logger, collector, selection, crossover, mutation):
    def fitness_real(ga_instance, solution, solution_idx):
        return 1. / func(solution)
    
    return pygad.GA(num_generations=config.num_generations,
            sol_per_pop=config.sol_per_pop,
            num_parents_mating=config.num_parents_mating,
            num_genes=config.num_genes,
            fitness_func=fitness_real,
            init_range_low=config.init_range_low,
            init_range_high=config.init_range_high,
            mutation_num_genes=config.mutation_num_genes,
            parent_selection_type=selection,
            crossover_type=crossover,
            mutation_type=mutation,
            keep_elitism= 1,
            K_tournament=3,
            random_mutation_max_val=32.768,
            random_mutation_min_val=-32.768,
            logger=logger,
            on_generation=collector.on_generation,
            parallel_processing=['thread', 4])

def binary_gad(config, func, logger, collector, selection, crossover, mutation):
    num_genes_binary = config.num_genes * config.num_bits_per_gene

    def fitness_func_binary(ga_instance, solution, solution_idx):
        decoded = decode_binary_solution(solution, config)
        fitness = func(decoded)
        return 1./fitness

    return pygad.GA(num_generations=config.num_generations,
        sol_per_pop=config.sol_per_pop,
        num_parents_mating=config.num_parents_mating,
        num_genes=num_genes_binary,
        fitness_func=fitness_func_binary,
        gene_space=[0, 1],  # <-- zamiast init_range_low / high
        gene_type=int,
        mutation_num_genes=config.mutation_num_genes,
        parent_selection_type=selection,
        crossover_type=crossover,
        mutation_type=mutation,
        keep_elitism= 1,
        K_tournament=3,
        logger=logger,
        on_generation=collector.on_generation,
        parallel_processing=['thread', 4])

def real_chromosome(config, func, logger):
    
    for selection in config.selections:
        for crossover in config.crossovers:
            for mutation in config.mutations:
                collector = GenerationStatsCollector()
                
                ga_instance = real_gad(config, func, logger, collector, selection, crossover, mutation)

                ga_instance.run()

                filename = f"wykresy-rzeczywiste/{selection}_{crossover}_{mutation}"

                collector.plot_diagram(filename, selection, crossover, mutation)

                solution, solution_fitness, solution_idx = ga_instance.best_solution()
                print("Parameters of the best solution : {solution}".format(solution=solution))
                print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=1./solution_fitness))
                print(f"Selection: {selection}\nCrossover: {crossover}\nMutation: {mutation} ")


                # sztuczka: odwracamy my narysował nam się oczekiwany wykres dla problemu minimalizacji
                ga_instance.best_solutions_fitness = [1. / x for x in ga_instance.best_solutions_fitness]

                plot_custom_fitness(ga_instance.best_solutions_fitness,f"Generation vs Fitness\nReal\n {selection}, {crossover}, {mutation}", filename)



def binary_chromosome(config, func, logger):
    for selection in config.selections:
        for crossover in config.crossovers:
            for mutation in config.mutations:
                collector = GenerationStatsCollector()

                ga_instance = binary_gad(config, func, logger, collector, selection, crossover, mutation)
            
                ga_instance.run()

                filename = f"wykresy-binarne/{selection}_{crossover}_{mutation}"

                collector.plot_diagram(filename, selection, crossover, mutation)

                solution, solution_fitness, solution_idx = ga_instance.best_solution()
                print("Parameters of the best solution : {solution}".format(solution=solution))
                print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=1./solution_fitness))
                print(f"Selection: {selection}\nCrossover: {crossover}\nMutation: {mutation} ")

                # sztuczka: odwracamy my narysował nam się oczekiwany wykres dla problemu minimalizacji
                ga_instance.best_solutions_fitness = [1. / x for x in ga_instance.best_solutions_fitness]

                plot_custom_fitness(ga_instance.best_solutions_fitness,f"Generation vs Fitness\nBinary\n {selection}, {crossover}, {mutation}", filename)


def run_all_combinations(config, func, logger):
    for selection in config.selections:
        for crossover in config.crossovers:
            for mutation in config.mutations:
                real_collector = GenerationStatsCollector()
                ga_real = real_gad(config, func, logger, real_collector, selection, crossover, mutation)
                ga_real.run()

                real_fitness = [1. / x for x in ga_real.best_solutions_fitness]

                binary_collector = GenerationStatsCollector()
                ga_binary = binary_gad(config, func, logger, binary_collector, selection, crossover, mutation)
                ga_binary.run()

                binary_fitness = [1. / x for x in ga_binary.best_solutions_fitness]

                filename = f"{selection}_{crossover}_{mutation}"
                plot_compare_fitness(real_fitness, binary_fitness, f"Generation vs Fitness\n{selection}, {crossover}, {mutation}", f"wykresy-porownawcze-wartosci/{filename}")

                print(f"\n--- {selection} | {crossover} | {mutation} ---")
                print("Best real:   ", ga_real.best_solution()[0])
                print("Fitness real:", 1. / ga_real.best_solution()[1])
                print("Best binary: ", ga_binary.best_solution()[0])
                print("Fitness bin: ", 1. / ga_binary.best_solution()[1])

                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

                real_collector.plot_diagram_on_ax(ax1, selection, crossover, mutation)
                ax1.set_title("Real")

                binary_collector.plot_diagram_on_ax(ax2, selection, crossover, mutation)
                ax2.set_title("Binary")

                fig.suptitle(f"Fitness per Generation\n{selection}, {crossover}, {mutation}", fontsize=14)
                plt.tight_layout(rect=[0, 0.03, 1, 0.95])

                plt.savefig(f"wykresy-porownawcze-statystyk/{selection}_{crossover}_{mutation}.png")
                plt.close()
                

def main():
    config = Config()
    logger = get_logger(config)
    
    os.makedirs("wykresy-binarne", exist_ok=True)
    os.makedirs("wykresy-rzeczywiste", exist_ok=True)
    os.makedirs("wykresy-porownawcze-wartosci", exist_ok=True)
    os.makedirs("wykresy-porownawcze-statystyk", exist_ok=True)

    func = bf.Hyperellipsoid(n_dimensions=config.num_genes)

    if config.chromosome_type == "both":
        run_all_combinations(config, func, logger)

    if config.chromosome_type == "real":
        real_chromosome(config, func, logger)
    
    if config.chromosome_type == "binary":
        binary_chromosome(config, func, logger)


if __name__ == "__main__":
    main()
