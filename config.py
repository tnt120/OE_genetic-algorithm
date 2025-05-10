from dataclasses import dataclass
import logging


@dataclass
class Config:
	chromosome_type="both" # "binary", "real", "both"
	logging_level = logging.DEBUG
	# Ustawienia binarnej reprezentacji
	num_genes = 8
	
	num_bits_per_gene = 16
	max_bin_value = 2**num_bits_per_gene - 1

	num_generations = 1200
	sol_per_pop = 80
	num_parents_mating = 50
	#boundary = func.suggested_bounds() #możemy wziąć stąd zakresy
	init_range_low = -32.768
	init_range_high = 32.768
	# init_range_low = 0,
	# init_range_high = 2
	mutation_num_genes = 1
	random_seed = 2137

	selections = ["tournament", "rws", "random"]
	crossovers = ["uniform", "single_point", "two_points"]
	mutations = ["random", "swap"]