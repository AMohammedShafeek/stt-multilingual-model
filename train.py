# pyrefly: ignore [missing-import]
import librosa
import torch

from datasets import load_dataset

from transformers import (
    WhisperProcessor,
    WhisperForConditionalGeneration,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer
)

print("Loading Processor...")

processor = WhisperProcessor.from_pretrained(
    "openai/whisper-tiny"
)

print("Loading Model...")

model = WhisperForConditionalGeneration.from_pretrained(
    "openai/whisper-tiny"
)

model.to("cuda")

print("GPU:", torch.cuda.get_device_name(0))

# =========================
# LOAD DATASET
# =========================

dataset = load_dataset(
    "csv",
    data_files="dataset/metadata.csv"
)["train"]


def prepare_sample(sample):

    audio_path = (
        f"dataset/audio/{sample['file']}"
    )

    audio, sample_rate = librosa.load(
        audio_path,
        sr=16000
    )

    input_features = processor(
        audio,
        sampling_rate=16000,
        return_tensors="pt"
    ).input_features[0]

    labels = processor.tokenizer(
        sample["text"]
    ).input_ids

    return {
        "input_features": input_features,
        "labels": labels
    }


print("Preparing Dataset...")

dataset = dataset.map(
    prepare_sample
)

# Remove unused columns
dataset = dataset.remove_columns(
    ["file", "text"]
)

print(dataset)

# =========================
# TRAINING CONFIG
# =========================

training_args = Seq2SeqTrainingArguments(
    output_dir="./whisper-finetuned",
    per_device_train_batch_size=1,
    learning_rate=1e-5,
    num_train_epochs=5,
    logging_steps=1,
    save_steps=10,
    fp16=True
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

print("\nStarting Training...\n")

trainer.train()

print("\nTraining Completed!")

trainer.save_model(
    "./whisper-finetuned"
)

print("\nModel Saved!")