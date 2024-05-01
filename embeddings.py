import json
import os 
from openai import OpenAI

def get_api_key(): 
    api_keys_path = r"C:\\shared\\content\\config\\api-keys"
    openai_key_path = os.path.join(api_keys_path, "hackathon_openai_keys.json")
    openai_keys = json.load(open(openai_key_path))
    # we are team 10
    my_openai_key = openai_keys['team_10']

    return my_openai_key


def create_client(key): 
    return OpenAI(api_key=key)


def get_embedding(text_to_embed, openai):
   
    response = openai.embeddings.create(
        model= "text-embedding-ada-002",
        input=[text_to_embed]
    )
    
    return response.data



if __name__ == "__main__": 
    api_key = get_api_key()

    openai = create_client(key = api_key)
    text = "This is quite the sentence."

    embedding_raw = get_embedding(text, openai)

    print(embedding_raw)

    

