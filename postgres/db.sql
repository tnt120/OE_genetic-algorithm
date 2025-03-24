CREATE TABLE jobs (
    job_id UUID PRIMARY KEY,
    genes TEXT,
    x1 NUMERIC,
    x2 NUMERIC,
    elapsed_time NUMERIC,
    fitness NUMERIC
);

CREATE TABLE epochs (
    epoch_id SERIAL PRIMARY KEY,
    job_id UUID REFERENCES jobs(job_id),
    epoch_number INTEGER,
    genes TEXT,
    x1 NUMERIC,
    x2 NUMERIC,
    fitness NUMERIC
);
