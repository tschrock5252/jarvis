# jarvis/core/wakeword.py

import time
import struct
import pvporcupine
import pyaudio

from jarvis.config import WAKE_WORD_PATH, is_speaking
from jarvis.core.executor import handle_jarvis_command  # to trigger on wake

def listen_for_wake_word(access_key: str):
    """
    Continuously listens for the wake word using Porcupine.
    When detected, triggers the main command handling logic.
    """
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=[WAKE_WORD_PATH]
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Jarvis is now passively listening for wake word...")

    try:
        while True:
            if is_speaking.is_set():
                time.sleep(0.5)
                continue

            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm_unpacked)
            if keyword_index >= 0:
                print(f"Wake word detected! (index: {keyword_index})")
                handle_jarvis_command()

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        stream.stop_stream()
        stream.close()
        porcupine.delete()
        pa.terminate()

