import os
from dotenv import load_dotenv
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage, get_response_synthesizer
from llama_index.core.schema import TextNode
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from DirectoryChunker import DirectoryChunker

load_dotenv()

def get_index(nodes, index_name):
    index = None
    path_to_vdb = f'D:\AS2-e4ea5f1ce7b6ea77\Documents\{index_name}'
    if not os.path.exists(path_to_vdb):
        print("building index", index_name)
        index = VectorStoreIndex(nodes, show_progress=True)
        index.storage_context.persist(persist_dir=path_to_vdb)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=path_to_vdb)
        )

    return index


data_path = os.path.join("data","full_contract_txt")
text_chunks = DirectoryChunker(data_path).get_chunks()
print(f'Retrieved {len(text_chunks)} chunks of contract text content')
text_chunks = [doc.page_content for doc in text_chunks]
print("Creating nodes")
nodes = [TextNode(text=chunk) for chunk in text_chunks]
text_index = get_index(nodes, "contract_text_vector_data")
#configure retriever
retriever = VectorIndexRetriever(
    index = text_index,
    similarity_top_k=5
)
#configure response synthesizer
response_synthesizer = get_response_synthesizer(
    response_mode = 'refine'
)
#assemble query engine
text_vdb_engine =RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer
)
# https://docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/usage_pattern/