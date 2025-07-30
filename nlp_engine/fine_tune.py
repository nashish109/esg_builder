import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

def fine_tune_model():
    """
    A complete script to fine-tune a sentiment analysis model (e.g., FinBERT) on an ESG-specific dataset.
    
    NOTE: This script is a template and requires a suitable dataset.
    The 'financial_phrasebank' is used here as a placeholder.
    """
    
    # 1. Load a pre-trained tokenizer and model
    model_name = "ProsusAI/finbert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3) # Assuming 3 labels: positive, negative, neutral

    # 2. Load and preprocess the dataset
    # Replace 'financial_phrasebank' with a relevant ESG dataset when available
    dataset = load_dataset("financial_phrasebank", "sentences_allagree")
    
    def tokenize_function(examples):
        return tokenizer(examples["sentence"], padding="max_length", truncation=True)

    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    
    # Rename the 'label' column to 'labels' as expected by the Trainer
    tokenized_datasets = tokenized_datasets.rename_column("label", "labels")
    tokenized_datasets.set_format("torch")

    # Split the dataset into training and evaluation sets
    train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000)) # Using a subset for demonstration
    eval_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000, 1200))

    # 3. Define training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
    )

    # 4. Initialize the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )

    # 5. Start fine-tuning
    print("Starting model fine-tuning...")
    trainer.train()
    print("Fine-tuning complete.")

    # 6. Save the fine-tuned model
    fine_tuned_model_path = "./models/finbert-esg-sentiment"
    trainer.save_model(fine_tuned_model_path)
    tokenizer.save_pretrained(fine_tuned_model_path)
    print(f"Model saved to {fine_tuned_model_path}")

if __name__ == "__main__":
    # This will download the model and dataset, and run the fine-tuning process.
    # It can be resource-intensive and time-consuming.
    fine_tune_model()