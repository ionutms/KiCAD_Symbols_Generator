# Use a more stable Python image with better security profile
FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    build-base \
    gcc \
    g++ \
    musl-dev

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 8050

# Suppress the pandas FutureWarning about groupby
# ENV PYTHONWARNINGS="ignore::FutureWarning:plotly.express._core"

# Command to run the application (using JSON array format)
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8050} app:server"]