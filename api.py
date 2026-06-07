import sys
import os
import shutil
import asyncio
import logging
import gc
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel

# --- Log Capture Setup ---
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

log_queue = None
main_loop = None

class LogStream:
    def __init__(self, original_stream):
        self.original_stream = original_stream

    def write(self, data):
        self.original_stream.write(data)
        # Send to the queue safely using the captured main loop
        if data.strip() and log_queue is not None and main_loop is not None:
            try:
                main_loop.call_soon_threadsafe(log_queue.put_nowait, data)
            except Exception:
                pass

    def flush(self):
        self.original_stream.flush()

# Redirect standard output and errors to our capture stream
sys.stdout = LogStream(sys.stdout)
sys.stderr = LogStream(sys.stderr)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_model_name = "medium"
model = None

@app.on_event("startup")
async def startup_event():
    global log_queue, main_loop, model
    main_loop = asyncio.get_running_loop()
    log_queue = asyncio.Queue()
    print("Loading default Whisper Model (medium)...")
    # Load model synchronously on startup
    model = WhisperModel(current_model_name, device="cuda", compute_type="float16")
    print("Default model loaded successfully.")

from fastapi.responses import StreamingResponse

@app.get("/logs")
async def stream_logs():
    async def log_generator():
        yield "data: [SYSTEM] Frontend Terminal connected.\\n\\n"
        while True:
            log_message = await log_queue.get()
            # Properly format multiline logs for SSE
            formatted = "\\n".join([f"data: {line}" for line in log_message.splitlines()])
            if formatted:
                yield f"{formatted}\n\n"
            
    return StreamingResponse(log_generator(), media_type="text/event-stream")

@app.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    model_size: str = Form("medium"),
    target_language: str = Form("auto")
):
    global current_model_name, model
    print(f"\n[API] === NEW TRANSCRIPTION REQUEST ===")
    
    if model_size != current_model_name:
        print(f"[API] 0/3: Switching model from '{current_model_name}' to '{model_size}'...")
        del model
        gc.collect()
        print(f"[API] Loading Whisper Model ({model_size})...")
        model = WhisperModel(model_size, device="cuda", compute_type="float16")
        current_model_name = model_size
        print(f"[API] Model '{model_size}' loaded successfully.")
        
    print(f"[API] Received audio file: {audio.filename} ({audio.content_type})")
    temp_file_path = f"temp_{audio.filename}"
    try:
        print("[API] 1/3: Saving audio to temporary file...")
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        file_size = os.path.getsize(temp_file_path)
        print(f"[API] ✓ Audio saved successfully. File size: {file_size} bytes.")
        
        print(f"[API] 2/3: Dispatching audio to Whisper CUDA model ({model_size})...")
        # Run the heavy transcription process in a background thread to prevent freezing the server
        lang_arg = None if target_language == "auto" else target_language
        segments, info = await asyncio.to_thread(model.transcribe, temp_file_path, language=lang_arg)
        
        print(f"[API] ✓ Initial model processing complete.")
        print(f"[API] Model detected language '{info.language}' with probability {info.language_probability:.2f}")
        
        print("[API] 3/3: Decoding audio segments...")
        full_text = ""
        for segment in segments:
            line = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text.strip()}"
            print(f"[API]   ↳ {line}")
            full_text += line + "\n"
            
        print(f"[API] === TRANSCRIPTION FINISHED ===")
        print(f"[API] Text Output: '{full_text.strip()}'")
        
        return {
            "transcript": full_text.strip(),
            "language": info.language
        }
    except Exception as e:
        print(f"[ERROR] Transcribe Failed: {str(e)}")
        return {"error": str(e)}
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
