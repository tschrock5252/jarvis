import os
from collections import deque
from typing import List, Tuple

MAX_HISTORY = 10  # Can be configured externally if needed

class ConversationContext:
    def __init__(self, max_length: int = MAX_HISTORY):
        self.history = deque(maxlen=max_length)

    def add_turn(self, user: str, jarvis: str):
        self.history.append((user, jarvis))

    def get_prompt(self, new_input: str) -> str:
        prompt_lines = [f"User: {u}\nJarvis: {a}" for u, a in self.history]
        prompt_lines.append(f"User: {new_input}\nJarvis:")
        return "\n".join(prompt_lines)

    def clear(self):
        self.history.clear()

    def export_history(self) -> List[Tuple[str, str]]:
        return list(self.history)

