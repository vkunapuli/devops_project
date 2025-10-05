from mcp import ClientSession, StdioServerParameters
#from mcp.client.streamable_http import StreamableHTTPTransport, streamablehttp_client
from mcp.client.streamable_http import StreamableHTTPTransport, streamablehttp_client
import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_aws import ChatBedrockConverse


mcp_server_url = "http://localhost:8000/mcp"

llm = ChatBedrockConverse(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    region_name ="us-east-1",
    temperature=.2,
    # max_tokens=...,
    # other params...
)

def display_message_info(messages):
   for message in messages:
       content = message.content
       if isinstance(content,  str):
           print(f"Content: {content}\n")
       elif isinstance(message, list):
           for item in content:
               if item['type'] == 'text':
                   print(f"Message ID: {message['id']}")
                   print(f"Text: {item['text']}\n")
               elif item['type'] == 'tool_use':
                   tool_name = item['name']
                   tool_input = item['input']
                   print(f"Using {tool_name} tool with input: {tool_input}\n")

async def run_agent():
    async with streamablehttp_client(mcp_server_url) as (read, write, extra):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            # Get tools
            tools = await load_mcp_tools(session)
            print("Welcome to MCP server, you can ask the following for any stock ticker \n \
                  1. Calculate short and long moving averages \n \
                  2. Calculate Relative Strength Index (RSI) \n \
                  3. Provide a comprehensive trade recommendation \n \
                  4. Analyze a ticker symbol \n \
                  5. Compare multiple ticker symbols \n \
                  6. Build a custom intraday trading strategy \n"
                )
            # Create and run the agent
            agent = create_react_agent(llm, tools)

            while True:
              print("Ask me about questions on Stock Market!:")
              query = input()
              agent_response = await agent.ainvoke({"messages": query})
              display_message_info(agent_response['messages'])

def display_message_info(messages):
   for message in messages:
       content = message.content
       if isinstance(content,  str):
           print(f"Content: {content}\n")
       elif isinstance(message, list):
           for item in content:
               if item['type'] == 'text':
                   print(f"Message ID: {message['id']}")
                   print(f"Text: {item['text']}\n")
               elif item['type'] == 'tool_use':
                   tool_name = item['name']
                   tool_input = item['input']
                   print(f"Using {tool_name} tool with input: {tool_input}\n")

if __name__ == "__main__":
    asyncio.run(run_agent())
