# jarvis/core/llm.py

import requests
from jarvis.config import OLLAMA_URL, OLLAMA_MODEL, MAX_HISTORY

# In-memory context store
conversation_history = []

def interpret_command(text, command_keys):
    """
    Uses LLaMA to determine if the spoken text matches a known command.
    Returns either the matching command string or 'none'.
    """
    command_list = "\n- " + "\n- ".join(command_keys)
    prompt = f"""
You are Jarvis, a voice assistant with the following exact commands:{command_list}

A user said: "{text}"

If this matches a command, respond ONLY with that exact command string. Otherwise, say "none".
"""

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })
        return response.json().get("response", "").strip().lower()
    except Exception as e:
        print(f"Ollama error (command matching): {e}")
        return "none"

def get_llama_response_with_context(user_input):
    """
    Sends the full conversation history to LLaMA and appends the latest exchange.
    Returns the assistant's response.
    """
    global conversation_history

    history = ""
    for u, a in conversation_history[-MAX_HISTORY:]:
        history += f"User: {u}\nJarvis: {a}\n"
    history += f"User: {user_input}\nJarvis:"

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": history,
            "stream": False
        })
        reply = response.json().get("response", "").strip()
        conversation_history.append((user_input, reply))
        if len(conversation_history) > MAX_HISTORY:
            conversation_history.pop(0)
        return reply
    except Exception as e:
        print(f"Ollama error (chat context): {e}")
        return "I'm having trouble connecting to the LLaMA model."
