from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.vectorstores.chroma import Chroma
from get_embeddings_function import get_embedding_function
from langchain_community.embeddings import OpenAIEmbeddings
import json
from langchain.prompts import ChatPromptTemplate
from openai import OpenAI

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

    def __init__(self, chroma_path):
        self._CHROMA_PATH = chroma_path
        self.db = Chroma(
            persist_directory=self._CHROMA_PATH, embedding_function=get_embedding_function()
        )
        #db.persist()

    def add_to_chroma_db(self, chunks: list[Document]):
        self.db.add_documents(chunks)
        self.db.persist()

    def get_all_embeddings(self):
        return self.db._collection.get(include=['embeddings'])
        
    def query(self, query_text: str):
        """QUERY CHROMA FOR RETRIVAL AUGMENTED GENERATION. RETURNS SIMILARITY SEARCH AND FILENAME."""
        PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""
        # Prepare the DB.
        embedding_function = get_embedding_function()
        
        # Search the DB.
        results = self.db.similarity_search_with_score(query_text, k=5)

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])[0:5000]
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        # print(prompt)
        sources = [doc.metadata.get("source", None) for doc, _ in results]
        #print(prompt)
        LLM = OpenAI( api_key=get_openai_key('C:/shared/content/config/api-keys/hackathon_openai_keys.json'))
        response = LLM.chat.completions.create(
        model='gpt-4',
        messages=[{'role': 'user', 'content': prompt}],)
        
        return {'response': response.choices[0].message.content, 'sources': sources}


