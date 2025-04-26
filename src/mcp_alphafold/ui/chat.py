import streamlit as st
import streamlit.components.v1 as components
from mcp_client import MCPClient


async def chat_ui(client: MCPClient):
    st.title("LLM Assistant with MCP Tools")
    st.write("Enter your query below to interact with the LLM and MCP tools.")
    st.title("Protein Viewer Bot")

    # --- Mock: simulate receiving .bcif URL from a backend tool call ---
    # In real usage, this would come from your MCP tool call result
    if "bcif_url" not in st.session_state:
        st.session_state["bcif_url"] = "https://alphafold.ebi.ac.uk/files/AF-Q01101-F1-model_v4.bcif"

    bcif_url = st.session_state["bcif_url"]

    # Show info or result of chatbot/tool interaction
    st.write("Protein structure retrieved:")
    st.code(bcif_url)

    # Display a button to show the 3D viewer
    if st.button("🔬 View 3D Structure"):
        molstar_html = f"""
        <div id="app" style="width:100%; height:500px;"></div>
        <script src="https://unpkg.com/molstar/build/viewer/molstar.js"></script>
        <script>
        const viewer = new MolStar.Viewer('app', {{
            layoutIsExpanded: true,
            layoutShowControls: true,
            layoutShowSequence: true,
            layoutShowLog: false,
            layoutShowLeftPanel: true
        }});

        viewer.loadStructureFromUrl('{bcif_url}', 'bcif');
        </script>
        """
        components.html(molstar_html, height=550)
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []

    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])

    # user_input = st.chat_input("Enter your prompt")
    # if user_input:
    #     st.session_state.messages.append({"role": "user", "content": user_input})

    #     with st.chat_message("user"):
    #         st.markdown(user_input)

    #     response = await client.process_query(user_input)
    #     st.session_state.messages.append({"role": "assistant", "content": response})

    #     with st.chat_message("assistant"):
    #         st.markdown(response)
