from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rich.logging import RichHandler
from config import Config
from db import PostgresConnector
from population import Population
from real_population import RealPopulation
import logging
import uuid

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger("genetic-algorithm")

db = PostgresConnector(dbname='postgres',
                       user='postgres',
                       password='some_passwd',
                       host='postgres',
                       port='5432')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/genetic/submit")
def genetic_submit(data: Optional[dict] = None):
    job_id = str(uuid.uuid4())

    logging.info(f"Starting job {job_id}")

    config = Config.from_request(data)
    if config.chromosome_type == "real":
        logging.info("Using real-valued chromosome representation")
        population = RealPopulation(config)
    else:
        population = Population(config)
    time, best_individual, history = population.try_solve()

    response = best_individual.to_dict()
    response['elapsed_time'] = time
    response['job_id'] = job_id
    response['history'] = [item["fitness"] for item in history]
    db.insert_job(job_id, response)

    db.insert_epochs(job_id, history)

    logging.info(f"Job {job_id} finished")
    return response
