import streamlit as st 
from CleanFile import CleanFile
import os

#begin = st.container()
#begin.title("Team Goldmine Presents ContractBot")

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
        



if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message ContractBot..."):
    st.chat_message("user").markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar: 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder_path = os.path.join(script_dir, r'data\full_contract_txt')
    for clean_file in get_clean_files():
        button_name = clean_file.filepath.replace(data_folder_path + '\\', '')
        st.button(button_name, key=button_name, on_click=show_contract_text_callback, args=[clean_file])