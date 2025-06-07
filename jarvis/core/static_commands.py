# jarvis/core/static_commands.py

STATIC_COMMANDS = {
    "open browser": lambda: print("Opening browser..."),  # Replace with actual subprocess if needed
    "say hello": lambda: print("Hello, Mr. Schrock."),
    "list files": lambda: print("Listing files..."),      # Replace with actual command if needed
    "show disk space": lambda: print("Showing disk space..."),  # Replace with actual command
    "shutdown": lambda: print("Pretend shutdown..."),
}

COMMAND_VOICES = {
    "open browser": "Opening your browser, sir.",
    "say hello": "Hello, Mr. Schrock.",
    "list files": "Here are your files.",
    "show disk space": "Displaying disk usage, sir.",
    "shutdown": "Initiating shutdown protocol... just kidding.",
}


def interpret_command(text: str) -> str:
    """
    Placeholder for command interpretation logic using a model or simple rule.
    """
    # Your real model-backed interpretation can go here
    lowered = text.lower()
    return lowered if lowered in STATIC_COMMANDS else "none"

