# jarvis/config.py

import threading

AUDIO_FILENAME = "jarvis_input.wav"
SHARED_WAV_PATH = "/mnt/jarvis/jarvis.wav"
WAKE_WORD = "jarvis"
OLLAMA_URL = "http://10.1.0.125:11434/api/generate"
OLLAMA_MODEL = "llama3"
PLAYBACK_LOCK_FILE = "/mnt/jarvis/playback.lock"
WAKE_WORD_PATH = "jarvis/assets/jarvis_linux.ppn"
MAX_HISTORY = 10

is_speaking = threading.Event()
