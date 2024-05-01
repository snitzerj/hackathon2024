from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.core.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context
# from note_engine import note_engine
from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from text_loader import text_vdb_engine
from csv_loader import create_csv_query_engine
from ChromaClient import ChromaClient
from get_full_contract_txt import get_full_contract_text
load_dotenv()

vector_client = ChromaClient('chroma5')
pandas_query_engine = create_csv_query_engine()
rag_query_tool = FunctionTool.from_defaults(fn=vector_client.query, description="this queries a vector database to retrieve relevant contract text context. When you use this tool, always return the sources used from the output.")
full_contract_content_tool = FunctionTool.from_defaults(fn=get_full_contract_text, description="this tool extracts the full content of a contract if a contract file name is given. This can help with summarization, comparison, and entity extraction tasks.")
tools = [
    # QueryEngineTool(
    #     query_engine=text_vdb_engine,
    #     metadata=ToolMetadata(
    #         name="contract_full_content_data",
    #         description="this queries a vector database to retrieve relevant contract text context",
    #     ),
    # ),
    pandas_query_engine,
    rag_query_tool,
    full_contract_content_tool
]



llm = OpenAI(model="gpt-4")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

if __name__ == "__main__": 
    while (prompt := input("Enter a prompt (q to quit): ")) != "q":
        result = agent.query(prompt)
        print(result)