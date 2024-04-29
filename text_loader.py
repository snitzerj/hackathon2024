from langchain_community.document_loaders import TextLoader
import os 
from langchain_text_splitters import CharacterTextSplitter

def load_text(file_path):
    loader = TextLoader(file_path, autodetect_encoding = True)
    doc = loader.load()
    return doc

def split_text(document): 
    text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=800,
    chunk_overlap=80,
    length_function=len,
    is_separator_regex=False,
)
    text = document.page_content
    return text_splitter.create_documents([text])
    
if __name__ == "__main__": 
    base_dir = r"data\\full_contract_txt"
    text_files = os.listdir(r"data\\full_contract_txt")
    sample_text_file = text_files[0]
    sample_file_path = os.path.join(base_dir, sample_text_file)
    docs = load_text(sample_file_path)

    chunks = split_text(docs[0])

    print(len(chunks))
    
