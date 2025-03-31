import psycopg2
import psycopg2.extras
import logging


class PostgresConnector:

    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(dbname=self.dbname,
                                         user=self.user,
                                         password=self.password,
                                         host=self.host,
                                         port=self.port)
            self.cursor = self.conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.Error as e:
            logging.error(f"Error connecting to PostgreSQL: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def insert_job(self, job_id, data: dict):
        if not self.conn or not self.cursor:
            logging.info("Database connection is not established.")
            return None

        try:
            self.cursor.execute(
                """
                INSERT INTO jobs (job_id, genes, points, elapsed_time, fitness)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING job_id;
                """,
                (job_id, data['genes'], data['points'],
                 data['elapsed_time'], data['fitness']),
            )
            self.conn.commit()
            return job_id
        except psycopg2.Error as e:
            self.conn.rollback()
            logging.info(f"Error inserting job: {e}")
            return None

    def insert_epochs(self, job_id, epoch_data_list):
        if not self.conn or not self.cursor:
            logging.debug("Database connection is not established.")
            return

        try:
            for epoch_data in epoch_data_list:
                self.cursor.execute(
                    """
                    INSERT INTO epochs (job_id, epoch_number, genes, points, fitness)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (
                        job_id,
                        epoch_data["epoch_number"],
                        epoch_data["genes"],
                        epoch_data['points'],
                        epoch_data["fitness"],
                    ),
                )
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            logging.error(f"Error inserting epochs: {e}")
