import numpy
import matplotlib.pyplot as plt

class GenerationStatsCollector:
	def __init__(self):
		self.generation_min = []
		self.generation_avg = []
		self.generation_std = []

	def on_generation(self, ga_instance):

		ga_instance.logger.info("Generation = {}".format(ga_instance.generations_completed))
		solution, solution_fitness, solution_idx = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)
		ga_instance.logger.info("Best    = {}".format(1. / solution_fitness))
		ga_instance.logger.info("Individual    = {}".format(repr(solution)))

		tmp = [1. / x for x in ga_instance.last_generation_fitness]

		min_val = numpy.min(tmp)
		avg_val = numpy.mean(tmp)
		std_val = numpy.std(tmp)

		self.generation_min.append(min_val)
		self.generation_avg.append(avg_val)
		self.generation_std.append(std_val)

		ga_instance.logger.info("Min    = {}".format(min_val))
		ga_instance.logger.info("Max    = {}".format(numpy.max(tmp)))
		ga_instance.logger.info("Average    = {}".format(numpy.average(tmp)))
		ga_instance.logger.info("Std    = {}".format(std_val))
		ga_instance.logger.info("\r\n")

	def plot_diagram(self, filename, selection, crossover, mutation):
		plt.figure(figsize=(10, 6))
		plt.plot(self.generation_min, label='Min')
		plt.plot(self.generation_avg, label='Average')
		plt.plot(self.generation_std, label='Std Dev')
		plt.title(f'Funkcja celu w kolejnych generacjach\nSelection: {selection}, Crossover: {crossover}, Mutation: {mutation}')
		plt.xlabel('Generacja')
		plt.ylabel('Wartość funkcji celu')
		plt.legend()
		plt.grid(True)
		plt.tight_layout()
		plt.savefig(f"{filename}_multi")
		plt.close()

		# Reset state for reuse
		self.generation_min.clear()
		self.generation_avg.clear()
		self.generation_std.clear()
		
	def plot_diagram_on_ax(self, ax, selection, crossover, mutation):
		ax.plot(self.generation_min, label='Min')
		ax.plot(self.generation_avg, label='Average')
		ax.plot(self.generation_std, label='Std Dev')
		ax.set_title(f'Selection: {selection}, Crossover: {crossover}, Mutation: {mutation}')
		ax.set_xlabel('Generacja')
		ax.set_ylabel('Wartość funkcji celu')
		ax.legend()
		ax.grid(True)