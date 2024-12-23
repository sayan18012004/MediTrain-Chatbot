from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

from .config import groq_api_key, model, system_prompt

client = ChatGroq(groq_api_key=groq_api_key, model_name=model)

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
