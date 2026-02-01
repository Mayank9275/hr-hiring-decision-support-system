import os
import shutil
from typing import List

from fastapi import FastAPI, UploadFile, File, Form

from Integration_Deployment.nlp_adapter import evaluate_resume as nlp_evaluate

app = FastAPI()

UPLOAD_DIR = "temp_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}


@app.post("/evaluate")
async def evaluate(
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    resume_paths = []

    for resume in resumes:
        file_path = os.path.join(UPLOAD_DIR, resume.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        resume_paths.append(file_path)

    result = nlp_evaluate(job_description, resume_paths)
    return result
