from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel, PeftConfig

app = Flask(__name__)

# Load the model and tokenizer
def load_model():
    adapter_path = "adapter_model"
    peft_config = PeftConfig.from_pretrained(adapter_path)
    base_model_name = "bagelnet/Llama-3-8B"

    quantization_config = BitsAndBytesConfig(
        load_in_8bit=True,
        llm_int8_threshold=6.0,
        llm_int8_has_fp16_weight=False,
    )

    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        quantization_config=quantization_config,
        device_map="auto",
        trust_remote_code=True
    )

    model = PeftModel.from_pretrained(base_model, adapter_path)
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    return model, tokenizer

model, tokenizer = load_model()

def generate_response(conversation_history, max_length=200):
    prompt = f"You are a helpful AI assistant. Provide a concise and relevant answer to the user's question. Only reply to the question\n\n{conversation_history}"
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=input_ids.shape[1] + max_length,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )

    response = tokenizer.decode(output[0][input_ids.shape[1]:], skip_special_tokens=True)
    return response.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    response = generate_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
