from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.vectorstores.chroma import Chroma
from get_embeddings_function import get_embedding_function

DATA_PATH = 'Contract_Data_Part_1/Supply'
CHROMA_PATH = "chroma"

def main():

    documents = load_documents()
    print(f"Number of documents loaded: {len(documents)}")
    chunks = split_documents(documents)
    print(f"Number of document chunks created: {len(chunks)}")
    add_to_chroma(chunks)

def load_documents():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )
    db.add_documents(chunks)
    db.persist()

main()

