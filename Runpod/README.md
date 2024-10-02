# Deploying Bakery Fine-Tuned Models on RunPod: A Comprehensive Guide

## Introduction

This guide provides step-by-step instructions for deploying Bakery fine-tuned models on RunPod. We'll use the llama3-8b model as an example, but the process is similar for other models.

## Prerequisites

- A RunPod account
- A GitHub account
- Familiarity with basic command-line operations
- Your Bakery API key

## Step 1: Create a RunPod Account

1. Visit https://www.runpod.io/console/signup to create your RunPod account.

![Screenshot 2024-10-01 at 9.24.12 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/08f6e446-3479-4ee8-8eb1-50e147f1f3ee/cdf2d6c3-2409-475f-bd59-5f368c74e394/Screenshot_2024-10-01_at_9.24.12_PM.png)

## Step 2: Deploy a New Pod

1. Log in to your RunPod account.
2. Navigate to the `Pods` section.
3. Click the `Deploy` button to create a new pod.
    
    ![Screenshot 2024-10-01 at 9.25.52 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/08f6e446-3479-4ee8-8eb1-50e147f1f3ee/a3c4f656-c510-421b-9ed6-702d7ba4691d/Screenshot_2024-10-01_at_9.25.52_PM.png)
    
4. Select the following configuration:
    - GPU: RTX 4000 Ada (20GB VRAM)
    - CPU: 9 cores
    - RAM: 39GB
    - Container template: `runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04`
    - Instance pricing: Spot ($0.19/hr as of this writing)
    
    ![Screenshot 2024-10-01 at 9.27.43 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/08f6e446-3479-4ee8-8eb1-50e147f1f3ee/8268cd10-ad6e-4239-bc74-4bb91adf64e8/Screenshot_2024-10-01_at_9.27.43_PM.png)
    
    ![Screenshot 2024-10-01 at 9.28.02 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/08f6e446-3479-4ee8-8eb1-50e147f1f3ee/27126021-4f26-45e4-92a0-5f0c74463441/Screenshot_2024-10-01_at_9.28.02_PM.png)
    
5. Click `Deploy Spot` to create the pod.

## Step 3: Prepare Your Application Code

1. Create a new GitHub repository for your application.
2. Develop a simple chatbot application or use an existing one.
3. Push your code to the GitHub repository.

Note: You can use the Bagel Client package to download the fine-tuned model directly to the instance.

## Step 4: Configure the RunPod Instance

1. In the RunPod console, locate your newly created pod.
2. Click "Edit pod" to modify the configuration.
    
    ![Screenshot 2024-10-01 at 9.56.58 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/08f6e446-3479-4ee8-8eb1-50e147f1f3ee/3bfa3f20-9975-42b8-8c1e-0a7da799e5c1/Screenshot_2024-10-01_at_9.56.58_PM.png)
    
3. Add HTTP ports as needed for your application.
4. Increase both the container disk and volume disk to 50GB.
    
    ![Screenshot 2024-10-01 at 9.58.01 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/08f6e446-3479-4ee8-8eb1-50e147f1f3ee/8da6a95f-6388-421e-9db4-0cdbeba2ab33/Screenshot_2024-10-01_at_9.58.01_PM.png)
    
5. Save the changes. The instance will restart automatically.

## Step 5: Connect to the RunPod Instance

1. In the RunPod console, click on your pod to open its details.
2. Use the provided web terminal to connect to your instance.

![Screenshot 2024-10-01 at 10.00.04 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/08f6e446-3479-4ee8-8eb1-50e147f1f3ee/16ae6e25-7535-41fa-b446-3a33de617418/Screenshot_2024-10-01_at_10.00.04_PM.png)

## Step 6: Set Up Your Environment

1. Clone your GitHub repository:
    
    ```
    git clone <your-repo-url>
    ```
    
2. Navigate to your project directory:
    
    ```
    cd <your-project-directory>
    ```
    
3. Install the required dependencies:
    
    ```
    pip install -r requirements.txt
    ```
    

## Step 7: Download the Fine-Tuned Model

Use the following Python script to download your fine-tuned model from Bakery:

```jsx
import os
import bagel
from getpass import getpass

def download_adapter_model(model_id, output_dir="adapter_model"):
    # Initialize the BagelML client
    client = bagel.Client()

    # Set up the API key
    if 'BAGEL_API_KEY' not in os.environ:
        api_key = getpass("Enter your BagelML API key: ")
        os.environ['BAGEL_API_KEY'] = api_key

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Download the model
    print(f"Downloading model {model_id}...")
    response = client.download_model(model_id)
    
    try:
        print(response)
        
        # Unzip the downloaded model
        import zipfile
        zip_path = f"{model_id}.zip"
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        
        # Remove the zip file
        os.remove(zip_path)
        
        print(f"Model extracted to {output_dir}")
    except:
        print("Failed to download the model")
        print(response)

if __name__ == "__main__":
    # Replace with your actual model ID
    model_id = input("Please enter your model id: ")
    download_adapter_model(model_id)
```

Save this script as `download_model.py` and run it:

```
python download_model.py
```

## Step 8: Run Your Application

1. Start your application:

```python
python app.py
```

Note: The first run may take some time as it initialises the model.

## Step 9: Access Your Application

1. In the RunPod console, find the "Connect" section for your pod.
2. Look for the HTTP port you configured earlier. e.g. `Connect to HTTP Service [Port 80]`
3. Use the provided URL to access your application.

![Screenshot 2024-10-01 at 10.00.04 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/08f6e446-3479-4ee8-8eb1-50e147f1f3ee/1c0a6ad0-d9ff-4bfe-8d45-0da4cd0fe578/Screenshot_2024-10-01_at_10.00.04_PM.png)

![Screenshot 2024-10-01 at 10.06.42 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/08f6e446-3479-4ee8-8eb1-50e147f1f3ee/ff316d12-6ca0-4f35-922a-d9949b46a65f/Screenshot_2024-10-01_at_10.06.42_PM.png)

## Conclusion

You have now successfully deployed your Bakery fine-tuned model on RunPod. This setup provides a powerful, scalable environment for running your AI applications.

## Additional Resources

- [RunPod Documentation](https://docs.runpod.io/)
- [Bagel Client Documentation](https://docs.bakery.bagel.net/bagel_py)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)

Remember to monitor your RunPod usage to manage costs effectively.