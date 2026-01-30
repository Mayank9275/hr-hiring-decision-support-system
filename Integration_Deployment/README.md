## NLP/ML Integration Details

### NLP Module Location
File: NLP_ML/engine/matcher.py

### Function to Call
rank_candidates(jd_text, resume_paths)

### Input
- jd_text: string (Job Description text)
- resume_paths: list of resume file paths

### Output (Dictionary)
{
  "final_score": float,
  "similarity_score": float,
  "skill_score": float,
  "experience_score": float,
  "matched_keywords": list,
  "missing_keywords": list,
  "remarks": string
}

