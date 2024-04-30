import pandas as pd
from dotenv import load_dotenv
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core import PromptTemplate
from llama_index.core.tools import QueryEngineTool 
from llama_index.core.tools import ToolMetadata

instruction_str = """\
    1. Convert the query to executable Python code using Pandas.
    2. The final line of code should be a Python expression that can be called with the `eval()` function.
    3. The code should represent a solution to the query.
    4. PRINT ONLY THE EXPRESSION.
    5. Do not quote the expression."""

new_prompt = PromptTemplate(
    """\
    You are working with a pandas dataframe in Python.
    The name of the dataframe is `df`.
    This is the result of `print(df.head())`:
    {df_str}

    Follow these instructions:
    {instruction_str}
    Query: {query_str}

    Expression: """
)

context = """Purpose: The primary role of this agent is to assist users by providing accurate 
            information about contracts. """

def create_csv_query_engine():

    load_dotenv()

    contracts_df = pd.read_csv('master_clauses.csv')

    contracts_query_engine = PandasQueryEngine(
        df=contracts_df, verbose=True, instruction_str=instruction_str
    )
    contracts_query_engine.update_prompts({"pandas_prompt": new_prompt})
    #contracts_query_engine.query("What is the Agreement Date-Answer for Document Name-Answer MARKETING AFFILIATE AGREEMENT")
    contracts_query_engine.query("What is the Parties column value for Document Name-Answer MARKETING AFFILIATE AGREEMENT")

    tools = [
        QueryEngineTool(
            query_engine=contracts_query_engine,
            metadata=ToolMetadata(
                name="contracts_data",
                description="this gives information about contracts",
            ),
        )
    ]

    return tools


