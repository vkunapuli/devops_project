from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from langchain_aws import ChatBedrockConverse
import re


retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id="1NOGOQUNFS",
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 10}},
    region_name ="us-east-1"
)


llm = ChatBedrockConverse(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    region_name ="us-east-1",
    temperature=.2,
    # max_tokens=...,
    # other params...
)

def query_llm(messages):
    global questions
    content = ''
    for chunk in llm.stream(messages):
       if chunk.content:
          content_text = chunk.content[0].get("text")
          if content_text is not None:
              content += chunk.content[0].get("text")
          print(chunk.content[0].get("text"), end='')
       if hasattr(chunk, 'usage_metadata') and isinstance(chunk.usage_metadata, dict):
          print(' ')
          # Attempt to get 'input_tokens' from the 'usage_metadata'
          input_tokens = chunk.usage_metadata.get('input_tokens', 0)
          output_tokens = chunk.usage_metadata.get('output_tokens', 0)
          print(f"tokens used : input-{input_tokens} output-{output_tokens}")
    return content   

def find_questions(text):
   # Regular expression pattern to match text between '. ' and '?'
   # pattern = r'\. (.*?)\?'
   pattern = r'(?:\. |\n)(.*?)(\?)'
   matches = re.findall(pattern, text)
   return matches

while True:
  print("Ask me about Seller Servicer  Guide!:")
  query = input()

  documents = retriever.invoke(query)

  system_prompt = """
  <task_description>
Your task is to determine the most relevant Section from Freddie Mac's "Single Family Seller Servicer Guide" to answer a given user question. The guide contains multiple individual Sections outlining requirements related to purchasing, selling, and servicing mortgages with Freddie Mac.
</task_description>

<instructions>
1. Read the <user_question>{{user_question}}</user_question> carefully.
2. Review the provided context, containing Sections from the "Freddie Mac Single Family Seller Servicer Guide".
3. Engage with the user by asking TWO follow-up questions to better understand their query and narrow down the most relevant Section.
4. Provide your final response in the following format:

<output_format>
Section name (in the format ####.#x, where # is a number denoting section header and x is a letter denoting subsection):
Verbatim restatement of the Section content:
Explanation for your choice of the most relevant Section:
</output_format>
</instructions>


<initial_prompt>Please provide the user question:</initial_prompt>
<response_1>{{response_1}}</response_1>

<follow_up_prompt>Based on the user's response, please ask a follow-up question to further narrow down the relevant Section:</follow_up_prompt>
<response_2>{{response_2}}</response_2>

<final_prompt>After considering the user's responses, please provide the most relevant Section name, verbatim Section content, and a clear explanation for your choice:</final_prompt>
  """

  messages = [
    (
        "system",
        system_prompt,
    ),
    ("user", f'Context: {documents}'),
    ("human", query),
  ]
  resp_content = query_llm(messages)
  questions = find_questions(resp_content)
  count = len(questions)
  while count:
    response = input()
    messages.append(("user", f"{response} for {questions[count-1]}" ))
    count -= 1
    if not count:
      questions = find_questions(query_llm(messages))
      count = len(questions)
