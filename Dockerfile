FROM python:3.10-slim

WORKDIR /app

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

ENV CMAKE_BUILD_PARALLEL_LEVEL=1

# Install setuptools first, then the models, to prevent the import crash
RUN pip install --no-cache-dir setuptools
RUN pip install --no-cache-dir git+https://github.com/ageitgey/face_recognition_models

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Force 1 worker so the AI models don't exceed 512MB RAM
CMD ["gunicorn", "--workers", "1", "--timeout", "120", "--preload", "--capture-output", "--log-level", "debug", "app:app", "--bind", "0.0.0.0:5000"]