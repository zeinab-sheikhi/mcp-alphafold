# import asyncio
# from datetime import datetime
# from typing import Any, Optional

# from mcp_alphafold.client.base import BaseMCPClient


# class ChatHandler:
#     """Handler for chat interactions with MCP client."""

#     def __init__(self, client: BaseMCPClient):
#         self.client = client
#         self.message_history = []
#         self.is_running = False
#         self.last_interaction = None

#     async def process_query(self, query: str) -> str:
#         """Process a query using Claude and available tools."""
#         self.last_interaction = datetime.now()
#         self.message_history.append({"role": "user", "content": query})

#         try:
#             available_tools = await self.client.list_tools()

#             response = self.client.anthropic.messages.create(
#                 model=self.client.model, max_tokens=1000, messages=self.message_history, tools=available_tools
#             )

#             final_text = []
#             assistant_message_content = []

#             for content in response.content:
#                 if content.type == "text":
#                     final_text.append(content.text)
#                     assistant_message_content.append(content)
#                 elif content.type == "tool_use":
#                     result = await self.handle_tool_call(content)
#                     final_text.append(result)

#             return "\n".join(final_text)
#         except Exception as e:
#             return f"Error processing query: {str(e)}"

#     async def handle_tool_call(self, tool_content: Any) -> str:
#         """Handle a tool call from Claude."""
#         tool_result = await self.client.call_tool(tool_content.name, **tool_content.input)

#         self.message_history.extend(
#             [
#                 {"role": "assistant", "content": [tool_content]},
#                 {
#                     "role": "user",
#                     "content": [{"type": "tool_result", "tool_use_id": tool_content.id, "content": tool_result}],
#                 },
#             ]
#         )

#         response = self.client.anthropic.messages.create(
#             model=self.client.model, max_tokens=1000, messages=self.message_history, tools=await self.client.get_tools()
#         )

#         return response.content[0].text if response.content else ""

#     async def chat_loop(self, timeout: Optional[int] = None):
#         """Run an interactive chat loop."""
#         self.is_running = True
#         self.last_interaction = datetime.now()

#         print("\nMCP Chat Started!")
#         print("Commands:")
#         print("  'quit' or 'exit' - Exit the chat")
#         print("  'clear' - Clear message history")
#         print("  'help' - Show these commands")

#         while self.is_running:
#             try:
#                 if timeout and self.last_interaction:
#                     elapsed = (datetime.now() - self.last_interaction).seconds
#                     if elapsed > timeout:
#                         print("\nChat session timed out due to inactivity.")
#                         break

#                 query = await self._get_input("\nQuery: ")

#                 if await self._handle_command(query):
#                     continue

#                 print("\nProcessing...")
#                 response = await self.process_query(query)
#                 print(f"\nResponse: {response}")

#             except asyncio.CancelledError:
#                 print("\nChat session cancelled.")
#                 break
#             except Exception as e:
#                 print(f"\nError: {str(e)}")
#                 if await self._should_continue():
#                     continue
#                 break

#     async def _get_input(self, prompt: str) -> str:
#         """Get input asynchronously."""
#         return await asyncio.get_event_loop().run_in_executor(None, lambda: input(prompt).strip())

#     async def _handle_command(self, command: str) -> bool:
#         """Handle special commands."""
#         command = command.lower()

#         if command in ["quit", "exit"]:
#             self.is_running = False
#             print("\nExiting chat...")
#             return True

#         elif command == "clear":
#             self.message_history.clear()
#             print("\nMessage history cleared.")
#             return True

#         elif command == "help":
#             print("\nAvailable commands:")
#             print("  'quit' or 'exit' - Exit the chat")
#             print("  'clear' - Clear message history")
#             print("  'help' - Show these commands")
#             return True

#         return False

#     async def _should_continue(self) -> bool:
#         """Ask if the user wants to continue after an error."""
#         while True:
#             response = await self._get_input("\nDo you want to continue? (y/n): ").lower()
#             if response in ["y", "yes"]:
#                 return True
#             if response in ["n", "no"]:
#                 self.is_running = False
#                 return False
