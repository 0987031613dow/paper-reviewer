FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including poppler-utils for pdf2image
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    poppler-utils \
    build-essential \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
