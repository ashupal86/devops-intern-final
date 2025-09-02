# Use official MLflow image
FROM ghcr.io/mlflow/mlflow:v3.3.1

# Install dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install psycopg2
RUN pip install --no-cache-dir psycopg2-binary boto3

# Set working directory
WORKDIR /app/mlflow

# Expose MLflow port
EXPOSE 5000
