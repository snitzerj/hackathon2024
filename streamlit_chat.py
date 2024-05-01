import streamlit as st 
from ChromaClient import ChromaClient
from CleanFile import CleanFile
import os
from ai_agent_main import agent
import json
import sys
from io import StringIO
import threading

def capture_output(func):
    def wrapper(*args, **kwargs):
        # Redirect sys.stdout to a StringIO object
        original_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Call the original function
            result = func(*args, **kwargs)
            
            # Get the output from StringIO and store it in a variable
            captured_output = sys.stdout.getvalue()
            with st.expander("AI Agent Observations"):
                st.write(captured_output)
            
            # Restore sys.stdout
            sys.stdout = original_stdout
            
            return result
        except Exception as e:
            # Restore sys.stdout even if an exception occurs
            sys.stdout = original_stdout
            raise e
    
    return wrapper

#begin = st.container()
#begin.title("Team Goldmine Presents ContractBot")

@st.cache_resource
def get_chroma_client():
    return ChromaClient('chroma5')

vector_client = get_chroma_client()
@st.cache_data(hash_funcs={CleanFile: lambda f: f.file_contents})
def get_clean_files():
    clean_files = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder_path = os.path.join(script_dir, r'data\full_contract_txt')
    # Loop through all files in the folder

    for filename in os.listdir(data_folder_path):
        # Check if the current file is a regular file
        if os.path.isfile(os.path.join(data_folder_path, filename)):
            clean_file = CleanFile(os.path.join(data_folder_path, filename))
            clean_files.append(clean_file)
    return clean_files


def show_contract_text_callback(clean_file):
    response = clean_file.file_contents
    with st.chat_message("assistant"):
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

def show_contract_text(file):
    # Read and store the file content in session state
    file_content = read_file(file.filepath)
    st.session_state['display_content'] = file_content
    file_name = os.path.basename(file.filepath)
    st.session_state['content_label'] = file_name

def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()
    
@capture_output
def display_agent_thoughts(prompt):
    return agent.query(prompt)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Goldmine..."):
    st.chat_message("user").markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    if 1 == 0:
        result = vector_client.query(prompt)
        with st.chat_message("assistant"):
            st.markdown(result['response'])
            st.markdown(set(result['sources']))
            for source in result['sources']:
                if source is not None:
                    with st.container():
                        with open(source, 'r') as file:
                            st.session_state['display_content'] = file.read()
                            st.session_state['content_label'] = source
                        with st.expander(f"{st.session_state['content_label']}\n", expanded=False):
                            st.write(st.session_state['display_content'])
        st.session_state.messages.append({"role": "assistant", "content": result['response']})
        st.session_state.messages.append({"role": "assistant", "content": set(result['sources'])})
    result = display_agent_thoughts(prompt)
    with st.chat_message("assistant"):
        print(f"LLM Query final result: {result}")
        result = json.loads(result.response)
        st.markdown(result['response'])
        st.markdown(set(result['sources']))
        for source in result['sources']:
            if source is not None:
                with st.container():
                    with open(os.path.join(r'data\full_contract_txt', source), 'r') as file:
                        st.session_state['display_content'] = file.read()
                        st.session_state['content_label'] = source
                    with st.expander(f"{st.session_state['content_label']}\n", expanded=False):
                        st.write(st.session_state['display_content'])
        
            

    st.session_state.messages.append({"role": "assistant", "content": result})


with st.sidebar: 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder_path = os.path.join(script_dir, r'data\full_contract_txt')
    for clean_file in get_clean_files():
        button_name = clean_file.filepath.replace(data_folder_path + '\\', '')
        st.button(button_name, key=button_name, on_click=show_contract_text, args=[clean_file])

# Main container for displaying the contract file contents
# if 'display_content' in st.session_state:
#     with st.container():
#         with st.expander(f"{st.session_state['content_label']}\n", expanded=False):
#             st.write(st.session_state['display_content'])
