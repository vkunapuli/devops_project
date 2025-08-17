from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from langchain_aws import ChatBedrockConverse

from collections import Counter
questions = 0

def load_file(filepath):
   """Load content from a text file."""
   try:
      with open(filepath, 'r', encoding='utf-8') as file:
          content = file.read()
   except UnicodeDecodeError:
       # Attempt with a different encoding
       with open(filepath, 'r', encoding='latin-1') as file:
          content = file.read()
   return content

def query_llm(messages):
    global questions
    for chunk in llm.stream(messages):
       if chunk.content:
          content_text = chunk.content[0].get("text")
          if content_text is not None and '?' in content_text:
              questions += 1
          print(chunk.content[0].get("text"), end='')
       if hasattr(chunk, 'usage_metadata') and isinstance(chunk.usage_metadata, dict):
          print(' ')
          # Attempt to get 'input_tokens' from the 'usage_metadata'
          input_tokens = chunk.usage_metadata.get('input_tokens', 0)
          output_tokens = chunk.usage_metadata.get('output_tokens', 0)
          print(f"tokens used : input-{input_tokens} output-{output_tokens}")

retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id="43CRETJELW",
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 10}},
    region_name ="us-east-1"
)


llm = ChatBedrockConverse(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    region_name ="us-east-1"
    # temperature=...,
    # max_tokens=...,
    # other params...
)

while True:
  print("Ask me about SS Guide!:")
  query = input()

  documents = retriever.invoke(query)
  s3_uris = []
  chapters = []

  for document in documents:
      uri = document.metadata['location']['s3Location'].get('uri')
      if uri:
         s3_uris.append(uri)
  for text in s3_uris:
      # Split by spaces and get the last item
      last_item = text.split()[-1]
      chapters.append(last_item)

  # Count occurrences of each item in the list
  counter = Counter(chapters)

  # Find the item with the maximum occurrences
  most_common_item, count = counter.most_common(1)[0]

  print(f"The most frequently referred chapter is '{most_common_item}' with {count} occurrences of {len(chapters)}.")

  filePath = '' 
  if most_common_item.startswith("Ch4"):
  # Load content from a file
     filepath = f'/home/ssm-user/devops_project/SSG/chapter_4xxx_pdf/Jun4Bulletin GF {most_common_item}'
  else: 
     filepath = f'/home/ssm-user/devops_project/SSG/chapter_5xxx_pdf/Jun4Bulletin GF {most_common_item}'
  print(filepath)
  file_content = load_file(filepath)

  system_prompt = """
  <task_description>
     Your task is to determine the most relevant Section from Freddie Mac's "Single Family Seller Servicer Guide" to answer a given user question. The guide contains multiple individual Sections outlining requirements related to purchasing, selling, and servicing mortgages with Freddie Mac.
  </task_description>

  <instructions>
    1. Read the <user_question>{{user_question}}</user_question> carefully.
    2. Review the provided attached document(s), containing Sections from the "Freddie Mac Single Family Seller Servicer Guide".
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
  #ai_msg = llm.invoke(messages)
  #print(ai_msg.content)
  query_llm(messages)
  while questions:
    response = input()
    questions -= 1
    messages.append(("user", f"user response {response}" ))
    if not questions:
      query_llm(messages)

