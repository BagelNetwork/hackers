# Bagel Finetuning Model Deployment with Docker

This repository provides a guide on how to deploy a fine-tuned model using Bagel with a Docker environment. It assumes you're working with **CUDA** and **NVIDIA GPUs** for model acceleration.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Building the Docker Image](#building-the-docker-image)
4. [Running the Container](#running-the-container)
5. [Troubleshooting](#troubleshooting)

## Prerequisites
Before you begin, ensure you have the following installed:
- **Docker** (with NVIDIA GPU support): [Docker installation guide](https://docs.docker.com/get-docker/)
- **BagelML API key**: You will need this to download your Bagel model.
- **Bagel Model ID**: You will need this to download your Bagel model.
- **NVIDIA CUDA Toolkit** (with appropriate drivers): Ensure your system is configured with GPU support.

## Setup

### 1. Clone this repository
```bash
git clone git@github.com:BagelNetwork/hackers.git
cd hackers/Docker
```

### 2. Configure your Model
This project uses a `model_downloader.py` script to download your Bagel finetuned model. Make sure you have your **BagelML API key** and **Bagel Model ID** ready.

Run the model downloader script:
```bash
python3 model_downloader.py
```

The script will prompt you for the model ID and API key, and then it will download and extract the model into the `adapter_model/` folder.

## Building the Docker Image

1. **Dockerfile** is already provided in the repository. It uses the **NVIDIA CUDA runtime** and installs necessary packages for your Flask application and the model.
   
2. Build the Docker image:
```bash
docker build -t chatbot .
```

This will create a Docker image called `chatbot`.

## Running the Container

Once the Docker image is built, you can run the container, mapping port 5000 from the container to your host.

### Run the Docker container with GPU support:
```bash
docker run --gpus all -p 5000:5000 chatbot
```

- This command uses all available GPUs (`--gpus all`).
- The Flask app will be running on **port 5000**.

### Access the Flask App:
Once the container is running, you can access the Flask application at:
```bash
http://localhost:5000
```
Change `localhost` to `your_machine_ip_address` if you want to access the app from outside the host machine.

You can also interact with the model via the `/chat` endpoint using GET requests.

## Troubleshooting

1. **Port is already in use**:
   If you encounter an error saying that port 5000 is already in use, stop any running containers that are using this port:
   ```bash
   docker ps
   docker stop <container_id>
   ```

2. **File Not Found**:
   If you encounter errors like `TemplateNotFound: index.html`, ensure that the `templates/` directory exists and contains the required HTML files.

3. **Model Loading Issues**:
   If you see `ValueError: Can't find 'adapter_config.json'`, verify that the `adapter_model` directory contains all required files after running the `model_downloader.py` script.

## License
This repository and the Docker container use the NVIDIA Deep Learning Container License. By using the container, you agree to the terms provided [here](https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license).
