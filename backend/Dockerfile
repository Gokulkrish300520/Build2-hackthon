# Dockerfile for backend (FastAPI)
FROM python:3.11-slim

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
	libgl1 \
	libglib2.0-0 \
	libx11-6 \
	libxcb1 \
	libsm6 \
	libxext6 \
	&& rm -rf /var/lib/apt/lists/*

# Clean up pip cache, __pycache__, .cache, and other unnecessary files after install
RUN pip cache purge || true && \
	find /usr/local/lib/python3.11/site-packages -type d -name '__pycache__' -exec rm -rf {} + && \
	rm -rf /root/.cache /root/.local /tmp/*

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Start the FastAPI app (adjust as needed)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
