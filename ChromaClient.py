from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.vectorstores.chroma import Chroma
from get_embeddings_function import get_embedding_function
from langchain_community.embeddings import OpenAIEmbeddings
import json

def get_openai_key(file_path):
    try:
        with open(file_path, 'r') as file:
            api_keys = json.load(file)
            openai_api_key = api_keys.get("team_10")
            return openai_api_key
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

def get_embedding_function():
    openai_api_key = get_openai_key('C:/shared/content/config/api-keys/hackathon_openai_keys.json')
    embeddings = OpenAIEmbeddings(
        openai_api_key=openai_api_key
    )
    # embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

class ChromaClient(object):

    def __init__(self):
        self._CHROMA_PATH = "chroma"
        self.db = Chroma(
            persist_directory=self._CHROMA_PATH, embedding_function=get_embedding_function()
        )
        #db.persist()

    def add_to_chroma_db(self, chunks: list[Document]):
        self.db.add_documents(chunks)
        self.db.persist()
        


