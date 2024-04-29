import re
from functools import lru_cache
from OpenAIClient import OpenAIClient
class CleanFile:
    
    def __init__(self, filepath):
        pattern = r'\s+'
        self.filepath = filepath
        try:
            with open(filepath) as file:
                    file_contents = file.read()
                    file_contents =  file_contents.rstrip('/r/n/0/t/f/v')
                    self.file_contents = re.sub(pattern, ' ', file_contents)
        except UnicodeDecodeError:
            self.file_contents = ''

    @lru_cache(maxsize=None)
    def get_vector_embedding(self):
        openai = OpenAIClient()
        return openai.get_embedding(self.file_contents)




