import json
import os 
from openai import OpenAI
class OpenAIClient:
    def get_api_key(): 
        api_keys_path = r"C:\\shared\\content\\config\\api-keys"
        openai_key_path = os.path.join(api_keys_path, "hackathon_openai_keys.json")
        openai_keys = json.load(open(openai_key_path))
        # we are team 10
        my_openai_key = openai_keys['team_10']

        return my_openai_key
    
    def __init__(self):
        self.api_key = self.get_api_key()
        self.client = OpenAI(api_key=self.api_key)


    def get_embedding(self, text_to_embed):
    
        response = self.client.embeddings.create(
            model= "text-embedding-ada-002",
            input=[text_to_embed]
        )
        
        return response.data




    

