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

# --- THIS IS THE MAGIC FIX ---
# Forces the C++ compiler to use only 1 thread, preventing the 8GB RAM crash
ENV CMAKE_BUILD_PARALLEL_LEVEL=1

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port
EXPOSE 5000

# Command to run your application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]