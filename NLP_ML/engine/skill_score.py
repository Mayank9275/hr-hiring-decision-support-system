from __future__ import annotations
import re
from typing import List, Set


def extract_required_skills_from_jd(jd_text: str) -> List[str]:
    """
    Extracts required skills from JD line like:
    "Required skills: Python, SQL, Machine Learning"
    """
    jd_text_lower = jd_text.lower()

    match = re.search(r"required skills\s*:\s*(.+)", jd_text_lower)
    if not match:
        return []

    skills_part = match.group(1)

    # Stop if next line contains "good to have" etc.
    skills_part = skills_part.split("good to have")[0]

    skills = [s.strip() for s in skills_part.split(",") if s.strip()]
    return skills


def skill_match_score(required_skills: List[str], resume_clean: str) -> float:
    """
    Score = matched_required_skills / total_required_skills
    """
    if not required_skills:
        return 0.0

    resume_set = set(resume_clean.split())

    matched = 0
    for skill in required_skills:
        # handle multiword skills like "machine learning"
        words = skill.split()
        if all(w in resume_set for w in words):
            matched += 1

    return matched / len(required_skills)
