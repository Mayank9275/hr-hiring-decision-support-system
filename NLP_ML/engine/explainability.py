from __future__ import annotations
from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer


def _top_terms(text: str, top_k: int = 12) -> List[str]:
    """
    Returns top TF-IDF terms from a single text.
    """
    vectorizer = TfidfVectorizer()
    vec = vectorizer.fit_transform([text])

    scores = vec.toarray()[0]
    terms = vectorizer.get_feature_names_out()

    term_scores = list(zip(terms, scores))
    term_scores.sort(key=lambda x: x[1], reverse=True)

    return [t for t, s in term_scores[:top_k] if s > 0]


def explain_match(jd_clean: str, resume_clean: str, top_k: int = 12) -> Tuple[List[str], List[str]]:
    """
    Returns:
    - matched_keywords: common important terms between JD and Resume
    - missing_keywords: important JD terms missing in Resume
    """
    jd_terms = set(_top_terms(jd_clean, top_k))
    resume_terms = set(_top_terms(resume_clean, top_k))

    matched = sorted(list(jd_terms.intersection(resume_terms)))
    missing = sorted(list(jd_terms - resume_terms))

    return matched, missing
