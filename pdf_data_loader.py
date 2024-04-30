import os
from dotenv import load_dotenv
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.readers import SimpleDirectoryReader
load_dotenv()

def get_index(data, index_name):
    index = None
    if not os.path.exists(index_name):
        print("building index", index_name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index


pdf_path = os.path.join("contract_pdf_vector_data")
reader = SimpleDirectoryReader(input_dir = pdf_path)
data = reader.load_data()
pdf_index = get_index(data, "contract_pdf_vector_data")
pdf_engine = pdf_index.as_query_engine()