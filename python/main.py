from population import Population
from config import Config

from rich.logging import RichHandler
import logging

# Configure pretty logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger("genetic-algorithm")

if __name__ == "__main__":
    config = Config()
    pop = Population(config)
    print("Start populacji:")
    print(pop)

    t, b, _ = pop.try_solve()

    print("\nFinalny wynik:")
    print(b)
    print(f"Czas wykonania: {t}s")
