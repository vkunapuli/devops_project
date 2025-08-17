from langchain_aws import ChatBedrockConverse

llm = ChatBedrockConverse(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    region_name ="us-east-1"
    # temperature=...,
    # max_tokens=...,
    # other params...
)
while True:
  print("Ask me anything!:")
  input1 = input()
  messages = [
    (
        "system",
        "You are a helpful assistant that will answer user question to the best of your ability",
    ),
    ("human", input1),
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
