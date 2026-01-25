from __future__ import annotations
import re


def extract_years(text: str) -> float:
    """
    Extracts years like '2 years', '3+ years', '1.5 years' from text.
    Returns max found value.
    """
    text = text.lower()
    matches = re.findall(r"(\d+(\.\d+)?)\s*\+?\s*years?", text)

    years = []
    for m in matches:
        years.append(float(m[0]))

    return max(years) if years else 0.0


def experience_match_score(jd_text: str, resume_text: str) -> float:
    """
    ExperienceScore = min(resume_years / required_years, 1.0)
    If JD does not mention years, returns 0.5 (neutral).
    """
    required_years = extract_years(jd_text)
    if required_years == 0:
        return 0.5  # neutral

    resume_years = extract_years(resume_text)
    return min(resume_years / required_years, 1.0)
