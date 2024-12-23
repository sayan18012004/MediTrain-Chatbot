import os
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.environ.get("GROQ_API_KEY")
model = "mixtral-8x7b-32768"  # Replace with a Groq medical-optimized model if available

system_prompt = (
    """
    You are a Doctor also give some advice to regular check up on health.
    Provide response in consistent manner around 50 words.
    """
)