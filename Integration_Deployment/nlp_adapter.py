from NLP_ML.engine.matcher import rank_candidates

def evaluate_resume(jd_text, resume_paths):
    """
    Adapter function for backend.
    Calls NLP/ML module and returns structured result.
    """
    result = rank_candidates(jd_text, resume_paths)

    return {
        "final_score": result.get("final_score"),
        "similarity_score": result.get("similarity_score"),
        "skill_score": result.get("skill_score"),
        "experience_score": result.get("experience_score"),
        "matched_keywords": result.get("matched_keywords"),
        "missing_keywords": result.get("missing_keywords"),
        "remarks": result.get("remarks"),
    }
