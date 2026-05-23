# pyrefly: ignore [missing-import]
from pydub import AudioSegment

audio = AudioSegment.from_file("dataset/audio/003.wav")

audio = audio.set_frame_rate(16000)
audio = audio.set_channels(1)

audio.export("dataset/audio/003_clean.wav", format="wav")