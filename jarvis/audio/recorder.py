# jarvis/audio/recorder.py

import wave
import time
import pyaudio
import threading
import whisper

from jarvis.config import AUDIO_FILENAME, is_speaking

def record_audio(duration=5, filename=AUDIO_FILENAME, rate=16000, channels=1):
    """
    Records audio from the default input device.
    Skips recording if Jarvis is currently speaking.
    """
    if is_speaking.is_set():
        print("Jarvis is speaking. Skipping recording...")
        return False

    print(f"Recording for {duration} seconds to {filename}...")

    try:
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paInt16,
                         channels=channels,
                         rate=rate,
                         input=True,
                         frames_per_buffer=1024)

        frames = []
        for _ in range(0, int(rate / 1024 * duration)):
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        pa.terminate()

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

        print("Recording saved.")
        return True

    except Exception as e:
        print(f"Recording failed: {e}")
        return False

def transcribe_file(filename):
    """
    Transcribes audio from the given file using Whisper.
    """
    try:
        model = whisper.load_model("base")
        result = model.transcribe(filename)
        return result["text"].strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""
