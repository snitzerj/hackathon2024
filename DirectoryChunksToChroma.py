from DirectoryChunker import DirectoryChunker
from ChromaClient import ChromaClient




data_folder_path = r'data\\some_contract_txt'
vector_client = ChromaClient('chroma5')
directory_chunker = DirectoryChunker(data_folder_path)

#print(directory_chunker.chunked_text[0].metadata)
#print(len(directory_chunker.get_chunks()))
vector_client.add_to_chroma_db(directory_chunker.get_chunks())
#print(chroma_client.get_all_embeddings())
print(vector_client.query("What is the definition of Launch Date?"))