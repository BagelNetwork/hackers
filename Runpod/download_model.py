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