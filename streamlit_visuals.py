import streamlit as st 
from CleanFile import CleanFile
import os
import pandas as pd
from streamlit_navigation_bar import st_navbar
import base64
#begin = st.container()
#begin.title("Team Goldmine Presents ContractBot")
########################################################################
# st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
#Navbar
pages = [""]
styles = {
    "nav": {
        "background-color": "#AF0808",
    },
    "div": {
        "max-width": "50rem",
    },
    "span": {
        "color": "white",
        "border-radius": "20.5rem",
        "padding": "20.4375rem 20.625rem",
        "margin": "10.125rem",
    },
    "active": {
        "background-color": "#AF0808",
    }
}

page = st_navbar(pages, styles=styles)
st.write(page)


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

# Define the HTML content for the logo and title
logo_html = """
<div style="display: flex; align-items: center;">
    <img src="https://example.com/logo.png" alt="Logo" width="50" height="50">
    <h1 style="color: white; margin: 0 0 0 10px;">My Streamlit App</h1>
</div>
"""




######################################################################

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