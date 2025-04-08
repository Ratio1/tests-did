# Dockerfile
FROM python:3.11-slim

# Set work directory
WORKDIR /app

COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code - requirement dont change often
COPY main.py .

CMD ["python3", "main.py"]