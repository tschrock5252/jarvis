# jarvis/main.py

import os
from dotenv import load_dotenv

from jarvis.core.wakeword import listen_for_wake_word

def main():
    # Load sensitive config like access keys from .env
    load_dotenv()
    access_key = os.getenv("PORCUPINE_ACCESS_KEY")

    if not access_key:
        raise ValueError("Missing PORCUPINE_ACCESS_KEY in .env file")

    # Start listening loop
    listen_for_wake_word(access_key)

if __name__ == "__main__":
    main()

