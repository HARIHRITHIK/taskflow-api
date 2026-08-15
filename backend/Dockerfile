FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Environment configuration
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application backend codebase
COPY . .

# Expose API port
EXPOSE 8000

# Launch Uvicorn ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
