import re
from functools import lru_cache
from OpenAIClient import OpenAIClient
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DirectoryChunker:
    def __init__(self, base_dir):
        text_list = self.load_text(base_dir)
        cleaned_text_list = self.clean_text(text_list)
        self.chunked_text = self.chunk_text(cleaned_text_list)
        
    def get_chunks(self): 
        return self.chunked_text
    
    @staticmethod
    def load_text(base_dir):
        text_loader_kwargs={'autodetect_encoding': True}
        loader = DirectoryLoader(base_dir, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
        return [doc.page_content for doc in loader.load()]
    
    @staticmethod
    def clean_text(text_list): 
        def _clean_text(text): 
            file_contents =  text.rstrip('/r/n/0/t/f/v')
            pattern = r'\s+'
            return re.sub(pattern, ' ', file_contents)
        
        return [_clean_text(text) for text in text_list]
    
    @staticmethod
    def chunk_text(text_list): 
        separators=[
            "\n\n",
            "\n",
            " ",
            ".",
            ",",
        ]

        text_splitter = RecursiveCharacterTextSplitter(
        separators=separators, 
        chunk_size=1000,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
    )
        return text_splitter.create_documents(text_list)
    




