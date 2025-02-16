# train.py
import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
from huggingface_hub import login

# 🔹 Authenticate with Hugging Face
login()  # Will prompt for token if not logged in

# 🔹 Correct repository name (Replace with your username)
repo_name = "Samarth1401/mental-health-chatbot"

def tokenize_function(examples):
    """Tokenize dataset and apply padding/truncation."""
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token  # Fix padding issue
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

def main():
    model_name = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token  # Ensure padding token is set
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # 🔹 Load and tokenize dataset
    dataset = load_dataset('text', data_files={'train': "mental_health_data.txt"})
    tokenized_datasets = dataset.map(tokenize_function, batched=True, remove_columns=["text"])

    # 🔹 Data collator for padding & formatting
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    # 🔹 Training arguments
    training_args = TrainingArguments(
        output_dir="./fine_tuned_model",
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=2,
        save_steps=500,
        save_total_limit=2,
        prediction_loss_only=True,
        remove_unused_columns=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=tokenized_datasets["train"],
    )

    # 🔹 Train and save model
    trainer.train()
    trainer.save_model("./fine_tuned_model")
    tokenizer.save_pretrained("./fine_tuned_model")
    print("✅ Fine-tuned model saved successfully!")

    # 🔹 Upload to Hugging Face
    print("Uploading model to Hugging Face...")
    model.push_to_hub(repo_name)
    tokenizer.push_to_hub(repo_name)
    print(f"✅ Model successfully uploaded: https://huggingface.co/{repo_name}")

if __name__ == "__main__":
    main()
