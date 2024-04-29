import json
import os 

api_keys_path = r"C:\\shared\\content\\config\\api-keys"
openai_key_path = os.path.join(api_keys_path, "hackathon_openai_keys.json")
openai_keys = json.load(open(openai_key_path))
# we are team 10
my_openai_key = openai_keys['team_10']

print(my_openai_key)
