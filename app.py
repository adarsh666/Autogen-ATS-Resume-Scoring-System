import streamlit as st
import uuid
from custom_tools.tools import add_document_to_vectorstore
from utils.tools import get_text

if 'resume' not in st.session_state:
    st.session_state['resume'] = False
if 'jd' not in st.session_state:
    st.session_state['jd'] = False
if 'jd_text' not in st.session_state:
    st.session_state['jd_text'] = None

col1, col2 = st.columns(2)

with col1:
    resume = st.button("Run Resume Analysis Team")
    if resume:
        st.session_state['resume'] = True
        st.session_state['jd'] = False

with col2:
    jd = st.button("Add Job Description to vector store")
    if jd:
        st.session_state['jd'] = True
        st.write("Job Description added to vector store")
        st.session_state['resume'] = False

if st.session_state['jd']:
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.session_state['jd_text'] = get_text(uploaded_file)
        st.write(st.session_state['jd_text'])
        if st.button("Upload"):
            add_document_to_vectorstore(st.session_state['jd_text'], str(uuid.uuid4()))
            st.write("Successfully added to vector store")
            st.session_state['jd_text'] = None
if st.session_state['resume']:
    st.write("Resume analysis team is running")