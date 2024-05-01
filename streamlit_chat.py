import streamlit as st 
from ChromaClient import ChromaClient
from CleanFile import CleanFile
import os
from ai_agent_main import agent
import json
import sys
from io import StringIO
from streamlit_navigation_bar import st_navbar
import base64
import contextlib
import numpy as np
from PIL import Image


class CustomStdout:
    def __init__(self, original_stdout):
        self.original_stdout = original_stdout

    def write(self, s):
        #self.original_stdout.write(s)
        self.call_function(s)

    def call_function(self, s):
        print(f'Function called with: {s}', file=self.original_stdout)
        if not len(f'{s}') == 0:
            with st.chat_message("assistant"):
                st.write(f'{s}')

    def flush(self):
        pass

def function_to_call():
    print("Hello, World!")

@contextlib.contextmanager
def stdout_redirector():
    original_stdout = sys.stdout
    sys.stdout = CustomStdout(original_stdout)
    try:
        yield
    finally:
        sys.stdout = original_stdout

# Define navigation pages
pages = [""]

# Define CSS styles for navigation bar
styles1 = {
    "nav": {
        "background-color": "#AF0808",
    },
    "div": {
        "max-width": "50rem",
    },
    "span": {
        "color": "black",
        "border-radius": "120.5rem",
        "padding": "120.4375rem 20.625rem",
        "margin": "10.125rem",
    },
    "active": {
        "background-color": "#AF0808",
    }
}

# Read the SVG file
with open("VG.svg", "rb") as f:
    svg_bytes = f.read()

# Encode the SVG file to Base64
svg_base64_encoded = base64.b64encode(svg_bytes).decode("utf-8")

st.sidebar.markdown(
    f"""
    <style>
        /* Center-align the logo */
        .sidebar .sidebar-content {{
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            margin-top: 2000px; 
        }}

        /* Center the image horizontally and vertically */
        .sidebar img {{
            margin: auto;
      
        }}
    </style>
    """
    f"""
    <div>
        <img src="data:image/svg+xml;base64,{svg_base64_encoded}" width="250" alt="Logo"/>
    </div>
    """,
    unsafe_allow_html=True
)

# Render navigation bar
page = st_navbar(pages, styles=styles1)

# Apply selected page logic
if page == "":
    img_file_buffer = st.sidebar.file_uploader('Upload a PNG image', type='png')
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        img_array = np.array(image)
        st.sidebar.image(image,  use_column_width=True)
        
        


#color for background

ms = st.session_state

if "themes" not in ms: 
    ms.themes = {
        "current_theme": "light",
        "refreshed": True,
        
        "light": {
            "theme.base": "dark",
            "theme.backgroundColor": "#ffeed6",
            "theme.primaryColor": "black",
            "theme.secondaryBackgroundColor": "#AF0808",
            "theme.activeColor": "pink",   # remove
            "theme.inputTextColor": "pink",  # remove
            "theme.textColor": "white" #text for side
        }
    }

def ApplyLightTheme():
    light_theme = ms.themes["light"]
    for vkey, vval in light_theme.items(): 
        if vkey.startswith("theme"): 
            st._config.set_option(vkey, vval)

# Custom CSS to style active text and input text
custom_css = f"""
<style>
.stText {{
    color: {ms.themes['light']['theme.textColor']} !important;
}}
.stMarkdown p {{
    color: {ms.themes['light']['theme.primaryColor']} !important;
}}
.stTextInput input[type="text"] {{
    color: {ms.themes['light']['theme.inputTextColor']} !important;
}}
.stTextArea textarea {{
    color: {ms.themes['light']['theme.inputTextColor']} !important;
}}
.stButton>div>span>div {{
    color: {ms.themes['light']['theme.activeColor']} !important;
}}
</style>
"""

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #AF0808;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="stExpander"] > div:first-child {
    background-color: #f0f0f0;
}
</style>
""", unsafe_allow_html=True)

# Apply the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

ApplyLightTheme()



# Define the HTML content for the logo and title
logo_html = """
<div style="display: flex; align-items: center;">
    <img src="https://example.com/logo.png" alt="Logo" width="50" height="50">
    <h1 style="color: white; margin: 0 0 0 10px;">My Streamlit App</h1>
</div>
"""




######################################################################





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
    
#@capture_output
def display_agent_thoughts(prompt):
    with stdout_redirector():
        response = agent.query(prompt)
        return response
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Goldmine..."):
    st.chat_message("user").markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    result = display_agent_thoughts(prompt)
    with st.chat_message("assistant"):
        print(f"LLM Query final result: {result}")
        try:
            result = json.loads(result.response)
        except ValueError as e:
            result = {'response': result, 'sources': []}
        
        st.markdown(result['response'])
        #print(f'SOURCE: {result['sources']}')
        try:
            if isinstance(result['sources'], str):
                source = result['sources']
                if source is not None and not source == 'contracts_tabular_data':
                        with st.container():
                            with open(os.path.join(r'data\full_contract_txt', source), 'r') as file:
                                st.session_state['display_content'] = file.read()
                                st.session_state['content_label'] = source
                            with st.expander(f"{st.session_state['content_label']}\n", expanded=False):
                                st.write(st.session_state['display_content'])
            else:
                for source in result['sources']:
                    if source is not None and not 'contracts_tabular_data' in source:
                        with st.container():
                            with open(os.path.join(r'data\full_contract_txt', source), 'r') as file:
                                st.session_state['display_content'] = file.read()
                                st.session_state['content_label'] = source
                            with st.expander(f"{st.session_state['content_label']}\n", expanded=False):
                                st.write(st.session_state['display_content'])
        except:
            pass
        st.session_state.messages.append({"role": "assistant", "content": result['response']})
        



with st.sidebar: 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder_path = os.path.join(script_dir, r'data\full_contract_txt')
    for clean_file in get_clean_files():
        button_name = clean_file.filepath.replace(data_folder_path + '\\', '')
        st.button(button_name, key=button_name, on_click=show_contract_text, args=[clean_file])

# Main container for displaying the contract file contents
    if 'display_content' in st.session_state:
        with st.container():
            with st.expander(f"{st.session_state['content_label']}\n", expanded=False):
                st.write(st.session_state['display_content'])
