import re
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DirectoryChunker:
    def __init__(self, base_dir):
        text_list_source_tuples = self.load_text(base_dir)
        text_list, sources = zip(*text_list_source_tuples)
        assert len(text_list) == len(sources)
        print(sources)
        cleaned_text_list = self.clean_text(text_list)
        self.chunked_text = self.chunk_text(cleaned_text_list, sources)
        
    def get_chunks(self): 
        return self.chunked_text
    
    @staticmethod
    def load_text(base_dir):
        text_loader_kwargs={'autodetect_encoding': True}
        loader = DirectoryLoader(base_dir, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
        return [(doc.page_content, doc.metadata['source']) for doc in loader.load()]
    
    @staticmethod
    def clean_text(text_list): 
        def _clean_text(text): 
            file_contents =  text.rstrip('/r/n/0/t/f/v')
            pattern = r'\s+'
            return re.sub(pattern, ' ', file_contents)
        
        return [_clean_text(text) for text in text_list]
    
    @staticmethod
    def chunk_text(text_list, sources): 
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
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
        
        docs =  [Document(page_content=text_list[i], metadata = {"source" : sources[i].split("\\")[-1]} ) for i in range(len(text_list))]
        return text_splitter.split_documents(docs)




