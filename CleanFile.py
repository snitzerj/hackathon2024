import re
from functools import lru_cache
from OpenAIClient import OpenAIClient
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.text_splitter import CharacterTextSplitter
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
    

    def get_file_contents_as_split_document(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        docs = [Document(page_content=x) for x in text_splitter.split_text(self.file_contents)]
        return docs
        






