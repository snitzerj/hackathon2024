from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.core.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context
# from note_engine import note_engine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from text_loader import text_vdb_engine
from csv_loader import create_csv_query_engine

load_dotenv()

pandas_query_engine = create_csv_query_engine()

tools = [
    QueryEngineTool(
        query_engine=text_vdb_engine,
        metadata=ToolMetadata(
            name="contract_full_content_data",
            description="this queries a vector database to retrieve relevant contract text context",
        ),
    ),
    pandas_query_engine
]

llm = OpenAI(model="gpt-3.5-turbo-0613")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    result = agent.query(prompt)
    print(result)