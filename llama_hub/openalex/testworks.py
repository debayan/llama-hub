#from llama_hub.semanticscholar.base import OpenAlexReader
from base import OpenAlexWorksReader
import os
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
oareader = OpenAlexReader()

# initialize the service context
openai.api_key = os.environ["OPENAI_API_KEY"]
service_context = ServiceContext.from_defaults(
    llm=OpenAI(model="gpt-3.5-turbo", temperature=0)
)

query_space = "large language models"

documents = oareader.load_data(query=query_space, limit=10)
index = VectorStoreIndex.from_documents(documents, service_context=service_context)
# initialize the citation query engine
query_engine = CitationQueryEngine.from_args(
    index,
    similarity_top_k=3,
    citation_chunk_size=512,
)

# query the citation query engine
response = query_engine.query("limitations of using large language models")
print("Answer: ", response)
print("Source nodes: ")
for node in response.source_nodes:
    print(node.node.metadata)
