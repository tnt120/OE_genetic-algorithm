import logging
import matplotlib.pyplot as plt

def decode_binary_solution(binary_solution, config, low=-32.768, high=32.768):
    real_solution = []
    for i in range(0, len(binary_solution), config.num_bits_per_gene):
        bits = binary_solution[i:i+config.num_bits_per_gene]
        int_val = int("".join(map(str, bits)), 2)
        real_val = low + (high - low) * (int_val / config.max_bin_value)
        real_solution.append(real_val)
    return real_solution

def get_logger(config):
    level = config.logging_level
    name = 'logfile.txt'
    logger = logging.getLogger(name)
    logger.setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_format = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

def plot_custom_fitness(fitness_values, title, filename):
    plt.figure()
    plt.plot(fitness_values)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    
def plot_compare_fitness(real, binary, title, filename):

    plt.figure(figsize=(10, 6))
    plt.plot(real, label="Real", color='blue')
    plt.plot(binary, label="Binary", color='red')
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{filename}.png")
    plt.close()