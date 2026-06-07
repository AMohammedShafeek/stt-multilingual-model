# pyrefly: ignore [missing-import]
import librosa

# pyrefly: ignore [missing-import]
from datasets import load_dataset

from transformers import WhisperProcessor

print("Loading processor...")

processor = WhisperProcessor.from_pretrained(
    "openai/whisper-tiny"
)

# =========================
# LOAD DATASET
# =========================

print("\nLoading dataset...")

dataset = load_dataset(
    "csv",
    data_files="dataset/metadata.csv"
)

dataset = dataset["train"]

print("\nDataset Loaded!")

print(dataset)

# =========================
# PREPROCESS FUNCTION
# =========================

def prepare_sample(sample):

    # Full audio path
    audio_path = (
        f"dataset/audio/{sample['file']}"
    )

    # Load audio
    audio, sample_rate = librosa.load(
        audio_path,
        sr=16000
    )

    # Audio → Features
    inputs = processor(
        audio,
        sampling_rate=16000,
        return_tensors="pt"
    )

    # Text → Token IDs
    labels = processor.tokenizer(
        sample["text"]
    ).input_ids

    return {
        "input_features":
            inputs.input_features[0],

        "labels":
            labels
    }

# =========================
# PROCESS DATASET
# =========================

print("\nProcessing dataset...")

processed_dataset = dataset.map(
    prepare_sample
)

print("\nDataset Processed Successfully!")

# =========================
# SHOW FIRST SAMPLE
# =========================

print("\nFirst Processed Sample:\n")

print(processed_dataset[0]["labels"])

print("\nKeys:")
print(processed_dataset[0].keys())