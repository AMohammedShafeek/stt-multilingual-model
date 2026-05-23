from transformers import WhisperProcessor

print("Loading Processor...")

processor = WhisperProcessor.from_pretrained(
    "openai/whisper-tiny"
)

print("\nProcessor Loaded Successfully!")

print("\nProcessor Details:\n")

print(processor)