from typing import Optional
from fastapi import FastAPI
from rich.logging import RichHandler
from config import Config
from population import Population
import logging
import uuid

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger("genetic-algorithm")

app = FastAPI()


@app.post("/genetic/submit")
def genetic_submit(data: Optional[dict] = None):
    data = data or {}
    config = Config(**{
        k: v
        for k, v in data.items() if k in Config.__annotations__
    })
    job_id = uuid.uuid4()
    logging.info(f"Starting job {job_id}")

    population = Population(config)
    time, best_individual, _ = population.try_solve()

    logging.info(f"Job {job_id} finished")

    response = best_individual.to_dict()
    response['elapsed_time'] = time
    response['job_id'] = job_id
    return response
