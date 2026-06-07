# pyrefly: ignore [missing-import]
import librosa

from transformers import WhisperProcessor

print("Loading processor...")

processor = WhisperProcessor.from_pretrained(
    "openai/whisper-tiny"
)

# =========================
# LOAD AUDIO
# =========================

print("\nLoading audio...")

audio, sample_rate = librosa.load(
    "dataset/audio/001_clean.wav",
    sr=16000
)

print("Audio Loaded!")

# =========================
# AUDIO → FEATURES
# =========================

print("\nConverting audio to features...")

inputs = processor(
    audio,
    sampling_rate=16000,
    return_tensors="pt"
)

input_features = inputs.input_features

print("Feature Shape:")
print(input_features.shape)

# =========================
# TEXT → TOKENS
# =========================

text = "Hello, Welcome to chennai"

print("\nOriginal Text:")
print(text)

labels = processor.tokenizer(
    text
).input_ids

print("\nToken IDs:")
print(labels)

# =========================
# FINAL TRAINING SAMPLE
# =========================

training_sample = {
    "input_features": input_features,
    "labels": labels
}

print("\nTraining Sample Created Successfully!")

print("\nKeys:")
print(training_sample.keys())
