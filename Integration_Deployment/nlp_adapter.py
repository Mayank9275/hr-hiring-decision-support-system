from NLP_ML.engine.matcher import rank_candidates
import os
import shutil

UPLOAD_DIR = "uploaded_resumes"

def evaluate_resume(job_description, resumes):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    resume_paths = []

    for resume in resumes:
        file_path = os.path.join(UPLOAD_DIR, resume.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        resume_paths.append(file_path)

    results = rank_candidates(job_description, resume_paths)

    return {
        "job_description": job_description,
        "ranked_candidates": results
    }
