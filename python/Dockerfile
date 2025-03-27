FROM python:3.13-slim-bookworm

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "2137" ]
