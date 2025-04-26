# import os
# from contextlib import AsyncExitStack
# from typing import Any, List, Optional

# from anthropic import Anthropic
# from dotenv import load_dotenv
# from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client

# load_dotenv()


# class MCPClient:
#     def __init__(self):
#         self.session: Optional[ClientSession] = None
#         self.exit_stack = AsyncExitStack()
#         self.anthropic = Anthropic()
#         self.model = "claude-3-5-sonnet-20241022"
#         self.system_prompt = self.read_system_prompt()
#         self.message_history = []

#     def read_system_prompt(self):
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         prompt_path = os.path.join(script_dir, "prompt.md")
#         try:
#             with open(prompt_path, "r") as file:
#                 return file.read()
#         except FileNotFoundError:
#             print(f"Error: The file {prompt_path} was not found.")
#             return ""

#     async def connect(self, server_script_path: str):
#         """Connect to an MCP server

#         Args:
#             server_script_path: Path to the server script (.py or .js)
#         """
#         server_params = StdioServerParameters(
#             command="python",
#             args=[server_script_path],
#             env=None,
#         )

#         stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
#         self.stdio, self.write = stdio_transport
#         self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
#         await self.session.initialize()

#     async def get_tools(self) -> List[Any]:
#         if not self.session:
#             raise RuntimeError("Not connected to MCP server")

#         response = await self.session.list_tools()

#         available_tools = [
#             {
#                 "name": tool.name,
#                 "description": tool.description,
#                 "input_schema": tool.inputSchema,
#             }
#             for tool in response.tools
#         ]
#         return available_tools

#     async def call_tool(self, tool_name: str, **kwargs) -> str:
#         if not self.session:
#             raise RuntimeError("Not connected to MCP server")

#         response = await self.session.call_tool(tool_name, arguments=kwargs)
#         return response.content[0].text if response.content else None

#     async def process_query(self, query: str) -> str:
#         """Process a query using Claude and available tools"""
#         self.message_history.append({"role": "user", "content": query})

#         available_tools = await self.get_tools()

#         # Initial Claude API call
#         response = self.anthropic.messages.create(
#             model=self.model,
#             max_tokens=1000,
#             messages=self.message_history,
#             tools=available_tools,
#             system=self.system_prompt,
#         )

#         # Process the response
#         final_text = []
#         assistant_message_content = []

#         for content in response.content:
#             if content.type == "text":
#                 final_text.append(content.text)
#                 assistant_message_content.append(content)
#             elif content.type == "tool_use":
#                 tool_name = content.name
#                 tool_args = content.input

#                 # execute tool call
#                 tool_result = await self.call_tool(tool_name, **tool_args)

#                 result_text = tool_result
#                 assistant_message_content.append(content)
#                 self.message_history.append(
#                     {
#                         "role": "assistant",
#                         "content": assistant_message_content,
#                     }
#                 )
#                 self.message_history.append(
#                     {
#                         "role": "user",
#                         "content": [
#                             {
#                                 "type": "tool_result",
#                                 "tool_use_id": content.id,
#                                 "content": result_text,
#                             }
#                         ],
#                     }
#                 )

#                 # Get next response from Claude
#                 response = self.anthropic.messages.create(
#                     model=self.model,
#                     max_tokens=1000,
#                     messages=self.message_history,
#                     tools=available_tools,
#                     system=self.system_prompt,
#                 )
#                 if response.content:
#                     final_text.append(response.content[0].text)

#         return "\n".join(final_text)

#     async def chat_loop(self):
#         """Run an interactive chat loop"""
#         print("\nMCP Client Started!")
#         print("Type your queries or 'quit' to exit.")

#         while True:
#             try:
#                 query = input("\nQuery: ").strip()
#                 if query.lower() == "quit":
#                     break
#                 response = await self.process_query(query)
#                 print(f"\nResponse: {response}\n")
#             except Exception as e:
#                 print(f"Error: {str(e)}")

#     async def cleanup(self):
#         """Clean up resources"""
#         await self.exit_stack.aclose()
