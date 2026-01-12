# -*- coding: utf-8 -*-
import sounddevice as sd
import vosk
import json
import queue

# Load small English model (fast & accurate enough for commands)
model = vosk.Model(r"PRGPFAD\vosk-model-small-en-us")
recognizer = vosk.KaldiRecognizer(model, 16000)

# Queue for audio data
q = queue.Queue()

def write_command(command):
    """Write recognized command to file for Delphi to read."""
    with open(r"PRGPFAD\SpeechCommand\recognized_command.txt", "w", encoding="utf-8") as file:
        file.write(command)

def callback(indata, frames, time, status):
    """Callback to put microphone data into queue."""
    q.put(bytes(indata))

def recognize():
    """Start speech recognition loop."""
    print("Speak commands... (Ctrl+C to stop)")
    
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip().lower()
                print(f"Recognized: {text}")
                
                # Simple command matching (add more as needed)
                if any(word in text for word in ["next", "skip"]):
                    write_command("next")
                elif any(word in text for word in ["stop", "halt"]):
                    write_command("stop")
                elif any(word in text for word in ["pause", "hold"]):
                    write_command("pause")
                elif any(word in text for word in ["play", "start", "go"]):
                    write_command("play")

if __name__ == "__main__":
    try:
        recognize()
    except KeyboardInterrupt:
        print("Stopped by user.")