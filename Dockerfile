# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# IMPORTANT: Install the missing system libraries required by dlib and OpenCV
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libpng-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port your Flask/FastAPI app runs on (e.g., 5000 or 8000)
EXPOSE 5000

# Command to run your application (Adjust 'app:app' based on your entry point)
# If using Flask: gunicorn app:app --bind 0.0.0.0:5000
# If using FastAPI: uvicorn app:app --host 0.0.0.0 --port 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]