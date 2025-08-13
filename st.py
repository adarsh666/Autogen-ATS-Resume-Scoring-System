import streamlit as st
import fitz
import docx2txt
import asyncio
import json

from Agents.parser_agent import get_resume_parser_agent
from Agents.ats_scoring_agent import get_ATS_scoring_agent

if 'resume_data' not in st.session_state:
    st.session_state['resume_data'] = None
if 'parsed_resume' not in st.session_state:
    st.session_state['parsed_resume'] = None
if 'ats' not in st.session_state:
    st.session_state['ats'] = None


def extract_text_from_pdf(file):
    text = ""
    pdf_doc = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf_doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    return docx2txt.process(file)

def get_text(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == "pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif file_type == "docx":
        text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file format")
        text = None
    return text
    

async def main():
    st.title("📄 PDF / DOCX Text Extractor")

    uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

    if uploaded_file:
        show_button = st.button("Get details from resume")
        if show_button:
            st.session_state['resume_data'] = get_text(uploaded_file)
            parser_agent = get_resume_parser_agent()
            result = await parser_agent.run(task=st.session_state['resume_data'])
            st.session_state['parsed_resume']  = json.loads(result.messages[-1].content)
            st.subheader("Extracted info:")
            st.json(st.session_state['parsed_resume'] )

        uploaded_jd = st.file_uploader("Upload Job Description", type=["pdf", "docx"])
        if uploaded_jd:
            ats_button = st.button("Calculate ATS Score")
            if ats_button :
                ats_agent = get_ATS_scoring_agent()
                ats_result = await ats_agent.run(task=f"Resume: {st.session_state['resume_data']}\
                                             Job Description: {get_text(uploaded_jd)}")
                st.session_state['ats'] = json.loads(ats_result.messages[-1].content)
                st.json(st.session_state['ats'] )
            

            # st.text_area("Text Output", result_json, height=400)
        # save_button = st.button("Save to Memory")


if __name__ == "__main__":
    asyncio.run(main())
