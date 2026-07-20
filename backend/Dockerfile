# Stage 1: Runtime environment configuration
FROM python:3.11-slim AS runtime

WORKDIR /code

# Install system dependencies required for compiling certain Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy backend source architecture code
COPY ./app ./app

# Set environment paths and expose the API gateway port
ENV PYTHONPATH=/code
EXPOSE 8000

# Run Uvicorn production server bound to all network interfaces
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]