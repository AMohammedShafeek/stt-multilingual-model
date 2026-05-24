# pyrefly: ignore [missing-import]
from faster_whisper import WhisperModel

print("Loading Whisper Model...")

model = WhisperModel("medium", device="cpu")

print("Starting Transcription...\n")

segments, info = model.transcribe("dataset/audio/002_clean.wav")

print("Detected Language: ", info.language)

full_text = ""

print("\nTranscript:\n")

for segment in segments:
    line = (
        f"[{segment.start:.2f}s -> {segment.end:.2f}s]"
        f"{segment.text}"
    )

    print(line)

    full_text += segment.text + " "

with open(
    "transcripts/output.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(full_text)

print("\nTranscript saved successfully!")