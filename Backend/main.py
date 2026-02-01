
import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from Integration_Deployment.nlp_adapter import evaluate_resume
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}

@app.post("/evaluate")
async def evaluate_resume(
    
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    # 🔹 TEMP response (NLP engine will come later)
    return evaluate_resume(job_description, resumes)

