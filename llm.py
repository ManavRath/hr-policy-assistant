import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise EnvironmentError(
        "GROQ_API_KEY is not set. Please add it to your .env file."
    )

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=api_key
)