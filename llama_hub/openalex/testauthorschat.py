#from llama_hub.semanticscholar.base import OpenAlexReader
from base import OpenAlexAuthorsReader
import os
import requests
import openai
from llama_index.llms import OpenAI
from llama_index.query_engine import CitationQueryEngine
from llama_index import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    ServiceContext,
)

# initialize the SemanticScholarReader
oareader = OpenAlexAuthorsReader()

# initialize the service context
openai.api_key = os.environ["OPENAI_API_KEY"]
service_context = ServiceContext.from_defaults(
    llm=OpenAI(model="gpt-3.5-turbo", temperature=0)
)

query_space = "Debayan Banerjee"

documents = oareader.load_data(query=query_space, limit=10)
index = VectorStoreIndex.from_documents(documents, service_context=service_context)
# initialize the citation query engine
query_engine = CitationQueryEngine.from_args(
    index,
    similarity_top_k=30,
    citation_chunk_size=512,
)
chat_history = []
while True:
    # Get user input
    user_input = input("You: ")

    if user_input.lower() == 'exit':
        print("Chat ended.")
        break

    # Append user input to chat history
    #chat_history.append({"role": "system", "content": "You: " + user_input})

    # Generate a response
    response = query_engine.query(user_input)

    # Append AI response to chat history
    #chat_history.append({"role": "assistant", "content": "AI: " + response})

    # Print AI response
    print("AI:", response)
    #print("Source nodes: ")
    #for node in response.source_nodes:
    #    print(node.node.metadata)
