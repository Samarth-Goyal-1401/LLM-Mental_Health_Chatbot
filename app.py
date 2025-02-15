# app.py
from flask import Flask, request, jsonify, render_template
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import os

app = Flask(__name__)

# Check if a fine-tuned model exists; otherwise, use GPT-2 pre-trained model
model_dir = "./fine_tuned_model"
if os.path.exists(model_dir):
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForCausalLM.from_pretrained(model_dir)
else:
    model_name = "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

# Initialize a text-generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# In-memory conversation history for demonstration
conversation_history = []

def generate_response(user_message):
    # Create a simple prompt; you can incorporate conversation history if desired
    prompt = f"User: {user_message}\nBot:"
    response = generator(prompt, max_length=100, num_return_sequences=1)
    bot_message = response[0]['generated_text']
    # Optionally, post-process to remove echo of the prompt
    return bot_message

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["GET"])
def chat():
    user_message = request.args.get("msg", "")
    if not user_message:
        return jsonify({"response": "Please provide a message."})
    
    conversation_history.append({"role": "user", "content": user_message})
    bot_message = generate_response(user_message)
    conversation_history.append({"role": "bot", "content": bot_message})
    
    return jsonify({"response": bot_message})

if __name__ == "__main__":
    app.run(debug=True)
