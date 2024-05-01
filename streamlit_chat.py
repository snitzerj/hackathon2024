import streamlit as st 
from ChromaClient import ChromaClient
from CleanFile import CleanFile
import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

@st.cache_resource
def get_chroma_client():
    return ChromaClient('chroma2')

vector_client = get_chroma_client()

try:
    # Try to get the default app, if it already exists, this will not raise an error
    firebase_app = firebase_admin.get_app()
except ValueError:
    # If it does not exist, initialize it
    json_dir = os.path.dirname(os.path.abspath(__file__))
    json_dir_path = os.path.join(json_dir, r'firestore-key.json')
    cred = credentials.Certificate(f'{json_dir_path}')
    firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client(app=firebase_app)

# Function to get chat sessions
def get_chat_sessions():
    sessions = db.collection('chats').stream()
    return {session.id: session.to_dict() for session in sessions}

# # Function to add a message to Firestore
# def add_message(session_id, message):
#     doc_ref = db.collection('chats').document(session_id)
#     doc_ref.update({'messages': firestore.ArrayUnion([message])})


# def save_session_to_firestore(session_messages):
#     sessions_collection = db.collection('sessions')
#     sessions_collection.add({
#         'messages': session_messages
#     })

# def load_sessions_from_firestore():
#     sessions_collection = db.collection('sessions')
#     sessions_docs = sessions_collection.stream()

#     all_sessions = []
#     for session in sessions_docs:
#         all_sessions.append(session.to_dict()['messages'])
#     return all_sessions

def add_message(session_id, role, content, attachments=None):
    message_data = {
        'role': role,
        'content': content,
        'timestamp': firestore.SERVER_TIMESTAMP,
    }
    db.collection('sessions').document(session_id).collection('messages').add(message_data)

st.sidebar.title("Chat Sessions")
all_sessions = get_chat_sessions()
selected_session = st.sidebar.selectbox("Select a Session", list(all_sessions.keys()))

if st.sidebar.button("Start New Session"):
    new_session_id = datetime.now().isoformat()
    db.collection('sessions').document(new_session_id).set({"messages": []})
    selected_session = new_session_id

# Refresh button to update messages
if st.sidebar.button("Refresh Messages"):
    st.rerun()

# Main chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying messages from Firestore and their associated files
messages = [msg.to_dict() for msg in db.collection('sessions').document(selected_session).collection('messages').stream()]
for msg in messages:
    with st.chat_message(msg['role']):
        st.markdown(f"{msg['timestamp'].isoformat()}: {msg['content']}")
        if msg.get('source_files'):
            for source in msg['source_files']:
                with st.expander(f"Source: {source}", expanded=False):
                    with open(source, 'r') as file:
                        st.write(file.read())

# User input and AI interaction
if prompt := st.chat_input("Message ContractBot..."):
    st.chat_message("user").markdown(prompt)
    result = vector_client.query(prompt)
    source_files = result.get('sources', [])
    add_message(selected_session, "user", prompt, source_files)

    with st.chat_message("assistant"):
        st.markdown(result['response'])
        for source in source_files:
            if source is not None:
                with st.expander(f"Source: {source}", expanded=False):
                    with open(source, 'r') as file:
                        st.write(file.read())
    add_message(selected_session, "assistant", result['response'], source_files)



