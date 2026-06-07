# pyrefly: ignore [missing-import]
import librosa

from transformers import WhisperProcessor

print("Loading processor...")

processor = WhisperProcessor.from_pretrained(
    "openai/whisper-tiny"
)

print("Loading audio...")

audio, sample_rate = librosa.load(
    "dataset/audio/001_clean.wav",
    sr=16000
)

print("\nAudio Loaded!")

print("\nAudio Shape:")
print(audio.shape)

print("\nSample Rate:")
print(sample_rate)

print("\nConverting Audio To Features...")

inputs = processor(
    audio,
    sampling_rate=16000,
    return_tensors="pt"
)

print("\nFeature Tensor Shape:")

print(inputs.input_features.shape)