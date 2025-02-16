# upload_model.py
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

# 🔹 Log in to Hugging Face
login()  # This will prompt you to enter your Hugging Face token

# 🔹 Define your Hugging Face repo name (Replace with your actual username)
repo_name = "Samarth1401/mental-health-chatbot"

# 🔹 Load fine-tuned model from local directory
try:
    print("Loading fine-tuned model...")
    model = AutoModelForCausalLM.from_pretrained("./fine_tuned_model")
    tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_model")
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit(1)

# 🔹 Upload model & tokenizer to Hugging Face
print(f"Uploading model to Hugging Face: {repo_name}...")
try:
    model.push_to_hub(repo_name, commit_message="Re-uploading fine-tuned model")
    tokenizer.push_to_hub(repo_name, commit_message="Re-uploading tokenizer")
    print(f"✅ Model successfully uploaded: https://huggingface.co/{repo_name}")
except Exception as e:
    print(f"❌ Upload failed: {e}")
    exit(1)
