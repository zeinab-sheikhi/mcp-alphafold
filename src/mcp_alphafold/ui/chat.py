import streamlit as st
from mcp_client import MCPClient


async def chat_ui(client: MCPClient):
    st.title("LLM Assistant with MCP Tools")
    st.write("Enter your query below to interact with the LLM and MCP tools.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Enter your prompt")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        response = await client.process_query(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.markdown(response)
