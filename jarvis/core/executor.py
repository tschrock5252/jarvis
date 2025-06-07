# jarvis/core/executor.py

import os
from jarvis.audio.recorder import record_audio, transcribe_file
from jarvis.audio.tts import speak
from jarvis.core.static_commands import STATIC_COMMANDS, COMMAND_VOICES, interpret_command
from jarvis.core.llm import get_llama_response_with_context
from jarvis.utils.text_cleaner import clean_response_text
from jarvis.utils.text_cleaner import strip_wake_word

AUDIO_FILENAME = "jarvis_input.wav"

def execute_static_command(command: str):
    """
    Execute a known static command and provide verbal feedback.
    """
    voice_line = COMMAND_VOICES.get(command, f"Executing {command}, sir.")
    print(f"Executing: {command}")
    speak(voice_line)
    STATIC_COMMANDS[command]()

def interpret_and_execute(input_text: str):
    """
    Interpret the input and either execute a static command or get a LLaMA response.
    """
    input_text = input_text.strip().lower()
    if not input_text:
        print("No input text to process.")
        return

    if input_text in STATIC_COMMANDS:
        execute_static_command(input_text)
    else:
        response = get_llama_response_with_context(input_text)
        print(f"LLaMA says: {response}")
        speak(clean_response_text(response))

def handle_jarvis_command():
    """
    Called after the wake word is detected.
    Handles recording, transcribing, and acting on user speech.
    """
    if not record_audio(filename=AUDIO_FILENAME):
        return

    spoken = transcribe_file(AUDIO_FILENAME)
    print(f"\nYou said: {spoken}")

    cleaned_input = strip_wake_word(spoken)
    if not cleaned_input:
        print("No command after wake word.")
        return

    command_guess = interpret_command(cleaned_input)
    print(f"Interpreted command: {command_guess}")

    if command_guess in STATIC_COMMANDS:
        execute_static_command(command_guess)
    else:
        response = get_llama_response_with_context(cleaned_input)
        print(f"LLaMA says: {response}")
        speak(clean_response_text(response))

