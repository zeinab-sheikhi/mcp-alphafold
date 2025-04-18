import asyncio
import os
from client.mcp_client import MCPClient


async def run_client():
    # os.environ.pop("SSL_CERT_FILE", None)
    # client = MCPClient.stdio(command="python", args=["src/mcp_alphafold/mcp_server.py"])
    # chat_handler = await MCPClient.create_chat_session(client)
    # print("Connected to MCP server...")
    # while True:
    #     query = input("Enter your query or 'quit' to exit:\n")
    #     if query.lower() == "quit":
    #         break
    #     response = await chat_handler.process_query(query)
    #     print(response) 
    from tools.uniprot import search_uniprot
    from tools.models import UniProtSearchParams, UniProtSearchField
    
    search_params = UniProtSearchParams(
        query="insulinoma",  
        fields=[UniProtSearchField.ACCESSION, UniProtSearchField.PROTEIN_NAME],
        size=1,
    )

    # Call the search_uniprot function
    response = await search_uniprot(params=search_params)
    
    # Print or process the response
    print("UniProt Search Response:", response)


def main():
    asyncio.run(run_client())


if __name__ == "__main__":
    main()
