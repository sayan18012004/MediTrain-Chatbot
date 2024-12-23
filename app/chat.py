
def initialize_chat_history(session_state):
    """Initialize chat history in session state."""
    if "chat_history" not in session_state:
        session_state.chat_history = []

def append_to_chat_history(session_state, role, content):
    """Append a message to the chat history."""
    session_state.chat_history.append({"role": role, "content": content})
