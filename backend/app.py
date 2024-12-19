import os
from dotenv import load_dotenv
import streamlit as st
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

groq_api_key = os.environ.get("GROQ_API_KEY")
model = "mixtral-8x7b-32768"  # Replace with a Groq medical-optimized model if available

# Initialize Groq client
client = ChatGroq(groq_api_key=groq_api_key, model_name=model)

# System prompt for the chatbot
system_prompt = (
    "You are MedBot, an AI-powered medical assistant. Provide users with accurate, empathetic, and clear answers "
    "to their medical queries. Avoid giving diagnoses; instead, recommend users consult a healthcare professional "
    "for a proper diagnosis and treatment."
)

# Memory configuration
conversational_memory_length = 5

def get_response(user_input, chat_history):
    """Generates a response for the given user input."""
    messages = [
        SystemMessage(content=system_prompt)
    ] + [
        SystemMessage(content=message["content"]) if message["role"] == "assistant" else HumanMessagePromptTemplate.from_template(message["content"]) 
        for message in chat_history
    ]
    
    prompt = ChatPromptTemplate.from_messages(messages + [HumanMessagePromptTemplate.from_template("{human_input}")])
    
    conversation = LLMChain(
        llm=client,
        prompt=prompt,
        verbose=False,
    )
    response = conversation.predict(human_input=user_input)
    return response

# Streamlit UI
def main():
    st.set_page_config(page_title="MedBot - Medical Chatbot", page_icon="💊", layout="wide")

    st.title("💊 MediTrain - Your Medical Assistant")
    st.write(
        "MediTrain is here to provide accurate, empathetic, and clear answers to your medical queries. "
        "Please note: MedBot does not provide diagnoses. Always consult a healthcare professional for proper diagnosis and treatment."
    )

    # Chat history initialization
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for chat in st.session_state.chat_history:
        avatar = "🤖" if chat["role"] == "assistant" else "👤"
        st.chat_message(chat["role"], avatar=avatar).write(chat["content"])

    # User input
    user_input = st.chat_input("Ask your medical question here...")

    if user_input:
        # Append user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Generate response
        with st.spinner("MedBot is typing..."):
            try:
                bot_response = get_response(user_input, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            except Exception as e:
                bot_response = f"An error occurred: {e}"
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

        # Display response
        st.chat_message("assistant", avatar="🤖").write(bot_response)

if __name__ == "__main__":
    main()