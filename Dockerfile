FROM docker.io/python:3.10-slim

WORKDIR /app

# Install system dependencies (ffmpeg and imagemagick for animated image support to spritesheet)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg imagemagick tzdata && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy application files
COPY . .

# Expose default backend port
EXPOSE 19000

# Start application
WORKDIR /app/backend
CMD ["python", "app.py"]
