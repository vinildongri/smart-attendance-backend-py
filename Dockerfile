# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# IMPORTANT: Added 'git' so pip can download the missing models directly from GitHub
RUN apt-get update && apt-get install -y \
    git \
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

# Throttle the C++ compiler to 1 core so it doesn't crash Render's 8GB RAM limit
ENV CMAKE_BUILD_PARALLEL_LEVEL=1

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5000

# Command to run your application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
