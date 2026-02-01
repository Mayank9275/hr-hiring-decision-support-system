from NLP_ML.engine.matcher import rank_candidates

def evaluate_resume(job_description: str, resume_paths: list[str]):
    """
    Expects:
    - job_description: string
    - resume_paths: list of saved resume file paths
    """

    results = rank_candidates(job_description, resume_paths)

    return {
        "job_description": job_description,
        "ranked_candidates": results
    }
