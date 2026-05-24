from transformers import WhisperProcessor

print("Loading processor...")

processor = WhisperProcessor.from_pretrained(
    "openai/whisper-medium"
)

text = "Hello, Welcome to chennai"

print("\nOriginal Text:")
print(text)

tokens = processor.tokenizer(
    text
)

print("\nToken IDs:\n")

print(tokens.input_ids)