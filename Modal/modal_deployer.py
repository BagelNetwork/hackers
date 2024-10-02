from modal import Image, Mount, gpu, App, asgi_app
from peft import PeftModel, PeftConfig

app = App("llama3-chatbot-test")  # Renamed from modal_app to app

# Define the Modal image
image = (
    Image.debian_slim()
    .pip_install(
        "fastapi",
        "uvicorn",
        "transformers",
        "accelerate",
        "bitsandbytes",
        "peft",
        "torch",
        "bagelML==0.0.20"
    )
    .apt_install("unzip")
)

@app.function(
    image=image,
    gpu=gpu.T4(),
    timeout=36000,
    container_idle_timeout=1200,
    keep_warm=1
)
@asgi_app()
def fastapi_app():
    from fastapi import FastAPI, Request
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    from peft import PeftModel, PeftConfig
    import os
    import bagel
    import zipfile

    api = FastAPI()
    
    # Check CUDA availability
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA device: {torch.cuda.get_device_name(0)}")
    
    client = bagel.Client()
    model_id = "5be78190-54db-4d49-8e97-107d17041403"

    # Set up the API key
    if 'BAGEL_API_KEY' not in os.environ:
        api_key = "oWpGZFPSHwGPF7xJLaddTemcDBdJCXhL"
        os.environ['BAGEL_API_KEY'] = api_key
    
    response = client.download_model(model_id)
    if not os.path.exists("adapter_model"):
        os.makedirs("adapter_model")
    
    try:
        print(response)
        
        zip_path = f"{model_id}.zip"
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("adapter_model")
        
        os.remove(zip_path)
        print("Model extracted to adapter_model")
    except Exception as e:
        print(f"Failed to download the model: {e}")
        print(response)

    # Paths to your models
    base_model_name = "bagelnet/Llama-3-8B"       # Adapter model path
    adapter_path = "adapter_model"  # Base model path

    peft_config = PeftConfig.from_pretrained(adapter_path)

    # Quantization configuration (if needed)
    quantization_config = BitsAndBytesConfig(
        load_in_8bit=True,
        llm_int8_threshold=6.0,
        llm_int8_has_fp16_weight=False
    )

    # Load the base model
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        quantization_config=quantization_config,
        device_map="auto",
        trust_remote_code=True
    )

    # Load the PEFT model (adapter)
    model = PeftModel.from_pretrained(base_model, adapter_path)

    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)

    @api.post("/generate")
    async def generate(request: Request):
        data = await request.json()
        prompt = data['prompt']

        # Generate response
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=100)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return {"response": response}

    return api


if __name__ == "__main__":
    app.serve()
