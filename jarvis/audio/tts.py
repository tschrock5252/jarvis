# jarvis/audio/tts.py

import os
import time
import threading
from TTS.api import TTS

from jarvis.config import SHARED_WAV_PATH, PLAYBACK_LOCK_FILE, is_speaking

# Initialize TTS model (you can change model/speaker here)
tts_engine = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)

def speak(text: str, speaker: str = "p302"):
    """
    Converts text to speech, writes it to a shared WAV file,
    and waits for external system to finish playback.
    """
    def _speak():
        is_speaking.set()
        try:
            with open(PLAYBACK_LOCK_FILE, 'w') as f:
                f.write("playing")

            tts_engine.tts_to_file(text=text, file_path=SHARED_WAV_PATH, speaker=speaker)

            print("Waiting for Windows playback to complete...")
            waited = 0
            MAX_WAIT = 15  # seconds

            while os.path.exists(PLAYBACK_LOCK_FILE):
                try:
                    os.stat(PLAYBACK_LOCK_FILE)  # Force filesystem check
                except FileNotFoundError:
                    break  # Lock file was removed externally
                time.sleep(0.25)
                waited += 0.25
                if waited >= MAX_WAIT:
                    print("Timeout waiting for playback. Removing lock file.")
                    try:
                        os.remove(PLAYBACK_LOCK_FILE)
                    except FileNotFoundError:
                        pass
                    break

            print("Playback confirmed complete. Continuing...")

        except Exception as e:
            print(f"Speech error: {e}")
        finally:
            is_speaking.clear()

    thread = threading.Thread(target=_speak)
    thread.start()
    thread.join()
