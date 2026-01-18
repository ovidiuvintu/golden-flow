FROM python:3.13-slim

WORKDIR /app

# Install minimal system deps (if needed) and pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application sources (copy whole context into /app)
COPY . .

# Create data directory for uploads and DB
RUN mkdir -p /app/data /data

EXPOSE 4000

ENV PYTHONUNBUFFERED=1

# Run the app module directly (project files are copied to /app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]
