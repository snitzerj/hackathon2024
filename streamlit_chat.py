import streamlit as st 
from ChromaClient import ChromaClient

#begin = st.container()
#begin.title("Team Goldmine Presents ContractBot")

@st.cache_resource
def get_chroma_client():
    return ChromaClient('chroma2')

vector_client = get_chroma_client()


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message ContractBot..."):
    st.chat_message("user").markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    result = vector_client.query(prompt)
    with st.chat_message("assistant"):
        st.markdown(result['response'])
        st.markdown(set(result['sources']))
    st.session_state.messages.append({"role": "assistant", "content": result['response']})
    st.session_state.messages.append({"role": "assistant", "content": set(result['sources'])})
