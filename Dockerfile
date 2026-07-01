# Use official Python lightweight image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast dependency resolver)
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY app ./app

# Install python dependencies using uv
RUN uv pip install --system -r pyproject.toml

# Expose port
EXPOSE 8000

# Run FastAPI server
CMD ["python", "-m", "uvicorn", "app.fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]
