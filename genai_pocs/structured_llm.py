from typing import List

from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage

# Define a pydantic model to enforce the output structure
class Questions(BaseModel):
    questions: List[str] = Field(
        description="A list of sub-questions related to the input query."
    )

from langchain_aws import ChatBedrockConverse


llm = ChatBedrockConverse(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    region_name ="us-east-1"
    # temperature=...,
    # max_tokens=...,
    # other params...
)
# Create an instance of the model and enforce the output structure
structured_llm = llm.with_structured_output(Questions)

# Define the system prompt
system = """You are a helpful assistant that generates multiple sub-questions related to an input question. \n
The goal is to break down the input into a set of sub-problems / sub-questions that can be answered independently. \n"""

# Pass the question to the model
question = """What are the main components of an LLM-powered autonomous agent system?"""
questions = structured_llm.invoke([SystemMessage(content=system)]+[HumanMessage(content=question)])
print(questions)
