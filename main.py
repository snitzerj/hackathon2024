import json
import os
from CleanFile import CleanFile
import subprocess

api_keys_path = r"C:\\shared\\content\\config\\api-keys"
openai_key_path = os.path.join(api_keys_path, "hackathon_openai_keys.json")
openai_keys = json.load(open(openai_key_path))
# we are team 10
my_openai_key = openai_keys['team_10']

print(my_openai_key)

# Get the directory of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Relative path to the 'data' folder
data_folder_path = os.path.join(script_dir, r'data\\full_contract_txt')
# Loop through all files in the folder

clean_files = []
for filename in os.listdir(data_folder_path):
    # Check if the current file is a regular file
    if os.path.isfile(os.path.join(data_folder_path, filename)):
        clean_file = CleanFile(os.path.join(data_folder_path, filename))
        clean_files.append(clean_file)

print(clean_files[0].get_file_contents_as_split_document())  