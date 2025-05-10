import logging
from config import Config
from population import Population
from real_population import RealPopulation

from rich.logging import RichHandler

# Configure pretty logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger("genetic-algorithm")

def main():
    config = Config()
    
    # Choose population type based on configuration
    if config.chromosome_type == "real":
        logging.info("Using real-valued chromosome representation")
        pop = RealPopulation(config)
    else:
        logging.info("Using binary chromosome representation")
        pop = Population(config)

    try:
        time, best, history = pop.try_solve()
        logging.info(f"Time: {time}s")
        logging.info(f"Best solution: {best}")
        print(f"Typ: {config.chromosome_type}")
        print(f"Crossover: {config.crossover_type}")
        print(f"Mutation: {config.mutation_type}")
        print(f"Finalny wynik:")
        print(best)
        print(f"Czas wykonania: {time}s, {len(history)} epok")
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise e


if __name__ == "__main__":
    main()
