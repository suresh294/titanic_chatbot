import os
import pandas as pd
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
# Load Titanic dataset
df = pd.read_csv("data/titanic.csv")

# Initialize Groq model
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-120b",
    temperature=0
)

SYSTEM_PROMPT = """
You are a data analyst working with a pandas DataFrame called df
which contains the Titanic dataset.

IMPORTANT RULES:
- Do NOT return Python code.
- Do NOT show calculations.
- Do NOT assign variables.
- Do NOT show dataframe operations.
- Always compute internally and return only the final answer in plain English.
- Keep answers short and clear.

If the user asks for a histogram or visualization,
just describe what the chart would show in one sentence.
"""

def ask_agent(question: str):
    prompt = f"""
{SYSTEM_PROMPT}

Question:
{question}

Provide the final answer clearly.
"""

    response = llm.invoke(prompt)
    return response.content