import streamlit as st
from backend.chat import initialize_chat_history, append_to_chat_history
from backend.model import get_response

st.set_page_config(page_title="MediTrain - Medical Chatbot", page_icon="💊", layout="wide")

def render_ui():
    """Render the Streamlit UI."""
    st.title("💊 MediTrain - Your Medical Assistant")
    st.write(
        "MediTrain is here to provide accurate, empathetic, and clear answers to your medical queries. "
        "Please note: MediTrain does not provide diagnoses. Always consult a healthcare professional for proper diagnosis and treatment."
    )

    # Initialize chat history
    initialize_chat_history(st.session_state)

    # Display chat history
    for chat in st.session_state.chat_history:
        avatar = "🤖" if chat["role"] == "assistant" else "👤"
        st.chat_message(chat["role"], avatar=avatar).write(chat["content"])

    # User input
    user_input = st.chat_input("Ask your medical question here...")

    if user_input:
        # Append user message to chat history
        append_to_chat_history(st.session_state, "user", user_input)

        # Generate response
        with st.spinner("MediTrain is typing..."):
            try:
                bot_response = get_response(user_input, st.session_state.chat_history)
                append_to_chat_history(st.session_state, "assistant", bot_response)
            except Exception as e:
                bot_response = f"An error occurred: {e}"
                append_to_chat_history(st.session_state, "assistant", bot_response)

        # Display response
        st.chat_message("assistant", avatar="🤖").write(bot_response)
