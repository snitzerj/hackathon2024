import pandas as pd
from dotenv import load_dotenv
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core import PromptTemplate
from llama_index.core.tools import QueryEngineTool 
from llama_index.core.tools import ToolMetadata
from prompts import new_prompt, instruction_str, context

def create_csv_query_engine():

    load_dotenv()
    
    contracts_df = pd.read_csv('data/contract_tabular_data.csv')

    contracts_query_engine = PandasQueryEngine(
        df=contracts_df, verbose=True, instruction_str=instruction_str
    )
    contracts_query_engine.update_prompts({"pandas_prompt": new_prompt})
    #contracts_query_engine.query("What is the Agreement Date-Answer for Document Name-Answer MARKETING AFFILIATE AGREEMENT")
    # contracts_query_engine.query("What is the Parties column value for Document Name-Answer MARKETING AFFILIATE AGREEMENT")

   
    tool =  QueryEngineTool(
            query_engine=contracts_query_engine,
            metadata=ToolMetadata(
                name="contracts_tabular_data",
                description="this queries tabular data about contracts",
            ),
        )
    

    return tool


