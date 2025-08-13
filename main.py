import asyncio
import json
from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import JSONResponse

from Agents.parser_agent import get_resume_parser_agent
from Agents.ats_scoring_agent import get_ATS_scoring_agent
from Agents.jd_analysis_agent import get_jd_analysis_agent
from utils.tools import extract_text_from_uploaded_file


app = FastAPI(title="Resume Parser API", description="Upload and query documents in vector store")

@app.post("/extract-resume-info")
async def extract_info(file: UploadFile = File(...)):
    """
    Extracts relevant information from an uploaded resume file.

    Parameters:
        file (UploadFile): The uploaded resume file in formats like PDF or DOCX.

    Returns:
        JSONResponse:
            - 200 OK with extracted resume details in JSON format on success.
            - 500 Internal Server Error with error message on failure.
    """
    try:
        text = extract_text_from_uploaded_file(file)
        query = "Extract all the required details from the resume: "
        parser_agent = get_resume_parser_agent()
        result = await parser_agent.run(task=(query + text))
        result = json.loads(result.messages[-1].content)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    

@app.post("/get-ats-score")
async def get_ats_score(resume: UploadFile = File(...),
                    job_description: UploadFile = File(...)):
    """
    Extracts relevant information from an uploaded resume file.

    Parameters:
        file (UploadFile): The uploaded resume file in formats like PDF or DOCX.

    Returns:
        JSONResponse:
            - 200 OK with extracted resume details in JSON format on success.
            - 500 Internal Server Error with error message on failure.
    """
    try:
        resume_text = extract_text_from_uploaded_file(resume)
        jd_text = extract_text_from_uploaded_file(job_description)
        ats_agent = get_ATS_scoring_agent()
        ats_result = await ats_agent.run(task=f"Resume: {resume_text}\
                                             Job Description: {jd_text}")
        result = json.loads(ats_result.messages[-1].content)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.post("/get-jds")
async def get_jds(resume: UploadFile = File(...)):
    """
    Extracts relevant information from an uploaded resume file.
    """
    try:
        resume_text = extract_text_from_uploaded_file(resume)
        ats_agent = get_jd_analysis_agent()
        ats_result = await ats_agent.run(task=resume_text)
        result = json.loads(ats_result.messages[-1].content)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})