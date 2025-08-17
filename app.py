import streamlit as st
import PyPDF2
import io
import asyncio
from docx import Document
from dotenv import load_dotenv
from PIL import Image

from Agents.parser_agent import get_resume_parser_agent
from Agents.jd_analysis_agent import get_jd_analysis_agent
from teams.ats_team import getDataAnalyzerTeam
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from utils.docker_util import getDockerCommandLineExecutor,start_docker_container,stop_docker_container
from utils.tools import remove_files
load_dotenv() 

import os
os.getenv("OPENAI_API_KEY")
IMAGE_FOLDER = "temp"
remove_files(IMAGE_FOLDER)

st.set_page_config(page_title="ATS Resume Scoring", page_icon="📄")
st.title("📄 ATS Resume Scoring System - File Input")

# File uploader
uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt"])



def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def extract_text_from_upload(uploaded_file) -> str:
    """
    Extract text from an uploaded Streamlit file (PDF, DOCX, or TXT).
    Reads file bytes once, then routes by extension.
    """
    name = (uploaded_file.name or "").lower()
    ext = name.rsplit(".", 1)[-1] if "." in name else ""
    data = uploaded_file.read()  # read once
    if not data:
        return ""
    if ext == "pdf":
        reader = PyPDF2.PdfReader(io.BytesIO(data))
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n".join(pages).strip()
    elif ext == "docx":
        doc = Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs).strip()
    elif ext == "txt":
        # try utf-8, fallback to latin-1
        try:
            return data.decode("utf-8").strip()
        except UnicodeDecodeError:
            return data.decode("latin-1", errors="ignore").strip()
    else:
        raise ValueError(f"Unsupported file type: {ext}")

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'autogen_team_state' not in st.session_state:
    st.session_state.autogen_team_state = None

async def run_analyser_gpt(task):
    docker = getDockerCommandLineExecutor()
    team = getDataAnalyzerTeam(docker)
    
    try:
        if st.session_state.autogen_team_state is not None:
            await team.load_state(st.session_state.autogen_team_state)

        await start_docker_container(docker)

        async for message in team.run_stream(task=task):
            # print(message)
            if isinstance(message,TextMessage):
                if message.source.startswith('user'):
                    with st.chat_message('user',avatar='👤'):
                        st.markdown(message.content)
                elif message.source.startswith('resume_parser_agent'):
                    with st.chat_message('Resume parser',avatar='🤖'):
                        st.markdown("**Resume parser**")
                        st.json(message.content)
                elif message.source.startswith('mongodb_agent'):
                    with st.chat_message('Database Agent',avatar='🤖'):
                        st.markdown("**Database Agentr**")
                        st.markdown(message.content)
                elif message.source.startswith('ats_scoring_agent'):
                    with st.chat_message('ATS Scorer',avatar='👨‍💻'):
                        st.markdown('**ATS Scorer**')
                        st.json(message.content)
                elif message.source.startswith('job_description_analysis_agent'):
                    with st.chat_message('JD Analyzer',avatar='👨‍💻'):
                        st.markdown('**JD Analyzer**')
                        st.markdown(message.content)
                elif message.source.startswith('improvement_recommendation_agent'):
                    with st.chat_message('Improvement Agent',avatar='👨‍💻'):
                        st.markdown('**Improvement Agent**')
                        st.markdown(message.content)
                elif message.source.startswith('society_of_mind'):
                    with st.chat_message('Visualization Agent',avatar='👨‍💻'):
                        st.markdown('**Visualization Agent**')
                        st.markdown(message.content)
                st.session_state.messages.append(message.content)
                # st.markdown(f"{message.content}")

            elif isinstance(message,TaskResult):
                st.markdown(f'Stop Reason :{message.stop_reason}')

                st.session_state.messages.append(message.stop_reason)
        if os.path.exists(IMAGE_FOLDER):
            image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if len(image_files) > 0:
                for img_file in image_files[:2]:
                    img_path = os.path.join(IMAGE_FOLDER, img_file)
                    image = Image.open(img_path)
                    st.image(image, caption=img_file, use_column_width=True)

        st.session_state.autogen_team_state = await team.save_state()
            
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return e
    finally:
        await stop_docker_container(docker)

if uploaded_file is not None:
    text = extract_text_from_upload(uploaded_file)

    if not text:
        st.warning("No extractable text found in the uploaded file.")
    else:
        # Optional: limit very long inputs to avoid hitting context limits
        #max_chars = st.slider("Max characters to send to the model", 2000, 200000, 20000, step=1000)
        text_to_send = text# [:max_chars]

        if st.button("Run Agent Team"):
            parser_agent = get_jd_analysis_agent()
            error = asyncio.run(run_analyser_gpt(text_to_send))
            if error:
                st.error(f'An error occured: {error}')

