FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if required by playwright or pdfplumber
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the port Hugging Face Spaces uses by default
EXPOSE 7860

# Start FastAPI on port 8000 in the background, and Chainlit on 7860 in the foreground
CMD uvicorn backend.main:app --port 8000 --host 0.0.0.0 & chainlit run frontend/app.py --port 7860 --host 0.0.0.0
