from langchain_community.document_loaders import TextLoader, DirectoryLoader
import os 
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
from typing import List
import embeddings


def load_text(base_dir):
    text_loader_kwargs={'autodetect_encoding': True}
    loader = DirectoryLoader(base_dir, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
    return [doc.page_content for doc in loader.load()]


def clean_text(text_list): 
    def _clean_text(text): 
        file_contents =  text.rstrip('/r/n/0/t/f/v')
        pattern = r'\s+'
        return re.sub(pattern, ' ', file_contents)
        
    return [_clean_text(text) for text in text_list]


def split_text(text_list): 
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

    
if __name__ == "__main__": 
    base_dir = r"data\\full_contract_txt"
    text_list = load_text(base_dir)
    cleaned_text_list = clean_text(text_list)
    split_texts = split_text(cleaned_text_list)
    

    
    
