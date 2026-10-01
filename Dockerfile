# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Create a non-root user
RUN useradd -m -u 1000 appuser

# Install dependencies from requirements-lock.txt
COPY requirements-lock.txt /app/
RUN pip install --no-cache-dir -r requirements-lock.txt

# Copy application code and saved model
COPY main.py diabetes_model.pkl /app/

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose API port
EXPOSE 8000

# Start Uvicorn single worker process without reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
