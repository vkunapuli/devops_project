from langchain_aws import ChatBedrockConverse
from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate

llm = ChatBedrockConverse(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    region_name ="us-east-1"
    # temperature=...,
    # max_tokens=...,
    # other params...
)

question1 = """
Karen harvests all the pears from 20 trees that have 10 pears each. She throws a third of them away as they are rotten, and turns a quarter of the remaining ones into jam. How many pears are left?
"""
answer1 = """
First, let's calculate how many pears Karen harvests: it's 20 * 10 = 200. 
A third of the pears are rotten, so 200 * 1/3 = 66.67, or about 67 pears are discarded.
Thus, the remaining pears are 200 - 67 = 133.
Karen then makes jam from a quarter of the remaining pears, so 133 * 1/4 = 33.25, or about 33.
Therefore, Karen has 133 - 33 = 100 pears left.
"""

question2 = """
Sergei harvests 30 pear trees, each yielding 15 pears. He discards half of them due to rot, and turns half of the remaining pears into jam. How many are left?
"""
answer2 = """
First, let's calculate how many pears Sergei harvests: 30 * 15 = 450. 
Half are discarded due to rot, so 450 * 1/2 = 225 pears remain.
Sergei turns half into jam, so 225 * 1/2 = 112.5, or about 113. 
Therefore, Sergei has 225 - 113 = 112 pears left.
"""

# Create Few-shot Prompt Template for CoT
example_prompt = PromptTemplate(input_variables=["question", "answer"], template="{question}\n{answer}")

examples = [
    {"question": question1, "answer": answer1},
    {"question": question2, "answer": answer2},
]

cot_prompt = FewShotPromptTemplate(
   examples=examples,
   example_prompt=example_prompt,
   suffix="Use these examples to answer the following problem: {input}",
   input_variables=["input"]
)

instruction = """
Andy harvests all the tomatoes from 18 plants that have 7 tomatoes each. If he dries half the
tomatoes and turns a third of the remainder into marinara sauce, how many tomatoes are left?
"""

cot_text = cot_prompt.format(input=instruction)
print("=== Chain of Thought Prompt ===")
print(cot_text)

while True:
  print("Ask me anything!:")
  input1 = input()
  messages = [
    (
        "system",
        "You are a helpful assistant that will answer user question to the best of your ability",
    ),
    ("human", cot_text),
  ]
  #ai_msg = llm.invoke(messages)
  #print(ai_msg.content)
  for chunk in llm.stream(messages):
    if chunk.content:
       print(chunk.content[0].get("text"), end='')
    if hasattr(chunk, 'usage_metadata') and isinstance(chunk.usage_metadata, dict):
       print(' ')
       # Attempt to get 'input_tokens' from the 'usage_metadata'
       input_tokens = chunk.usage_metadata.get('input_tokens', 0)
       output_tokens = chunk.usage_metadata.get('output_tokens', 0)
       print(f"tokens used : input-{input_tokens} output-{output_tokens}")
