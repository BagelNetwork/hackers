FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

WORKDIR /app

# Install necessary packages including Python, pip, and libraries
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    libcusparse-11-8 \
    libcublas-11-8 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for CUDA
ENV PATH=/usr/local/cuda/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Copy requirements and install dependencies
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt \
    && pip3 install --no-cache-dir \
    numpy==1.23.5 \
    scipy \
    torch==2.0.1+cu118 \
    torchvision==0.15.2+cu118 \
    torchaudio==2.0.2 --extra-index-url https://download.pytorch.org/whl/cu118

# Copy the app source code
COPY . .

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Expose the application port
EXPOSE 5000

# Run the Flask application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

