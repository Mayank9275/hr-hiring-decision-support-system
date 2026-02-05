from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import shutil
import os

# import your NLP engine
from NLP_ML.engine.matcher import rank_candidates

app = FastAPI()

# ---- CORS (VERY IMPORTANT) ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"status": "Backend is running"}


@app.post("/analyze")
async def analyze_candidates(
    jd_text: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    resume_paths = []

    for file in resumes:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        resume_paths.append(file_path)

    results = rank_candidates(jd_text, resume_paths)
    return results

