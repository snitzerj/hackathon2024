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