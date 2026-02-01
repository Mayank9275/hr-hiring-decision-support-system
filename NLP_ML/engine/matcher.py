from __future__ import annotations
from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .resume_parser import extract_text
from .preprocess import preprocess_text
from .explainability import explain_match
from .skill_score import extract_required_skills_from_jd, skill_match_score
from .experience_score import experience_match_score




def rank_candidates(jd_text: str, resume_paths: List[str]) -> List[Dict]:
    # 1) Extract + preprocess resumes
    resumes_clean = []
    resumes_raw_text = []
    candidates = []

    for path in resume_paths:
        raw_text = extract_text(path)
        cleaned = preprocess_text(raw_text)

        resumes_raw_text.append(raw_text)
        resumes_clean.append(cleaned)

        candidates.append({
            "candidate_name": path.split("/")[-1],
            "resume_path": path
        })

    # 2) Preprocess JD
    jd_clean = preprocess_text(jd_text)

    # 3) TF-IDF vectorization
    corpus = [jd_clean] + resumes_clean
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # 4) Similarity
    jd_vector = tfidf_matrix[0]
    resume_vectors = tfidf_matrix[1:]
    similarity_scores = cosine_similarity(jd_vector, resume_vectors)[0]

    # 5) Required skills from JD
    required_skills = extract_required_skills_from_jd(jd_text)

    # 6) Build results
    results = []
    for i, sim in enumerate(similarity_scores):
        matched, missing = explain_match(jd_clean, resumes_clean[i], top_k=12)

        similarity_score = float(sim)
        skill_score = float(skill_match_score(required_skills, resumes_clean[i]))
        experience_score = float(experience_match_score(jd_text, resumes_raw_text[i]))

        final_score = (0.70 * similarity_score) + (0.20 * skill_score) + (0.10 * experience_score)

        if final_score >= 0.70:
            remarks = "Strong match"
        elif final_score >= 0.45:
            remarks = "Moderate match"
        else:
            remarks = "Weak match"

        results.append({
            "candidate_name": candidates[i]["candidate_name"],
            "resume_path": candidates[i]["resume_path"],

            "final_score": final_score,
            "similarity_score": similarity_score,
            "skill_score": skill_score,
            "experience_score": experience_score,

            "matched_keywords": matched,
            "missing_keywords": missing,
            "remarks": remarks
        })

    # 7) Sort by final score
    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results
