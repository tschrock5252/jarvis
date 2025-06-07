# jarvis/utils/text_cleaner.py

import re

def clean_response_text(text: str) -> str:
    """
    Cleans LLM output (e.g., Markdown symbols) before speaking.
    """
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'_+', '', text)
    text = re.sub(r'`+', '', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    return text.strip()

def strip_wake_word(text: str, wake_word: str = "jarvis") -> str:
    """
    Removes the wake word from the beginning of the transcribed text.
    """
    pattern = re.compile(rf"\b{wake_word}\b[:,]?\s*", re.IGNORECASE)
    return pattern.sub("", text).strip()
