from engine.matcher import rank_candidates

jd_text = """
We are hiring for an AI/ML Intern.
Required skills: Python, Machine Learning, SQL, Data Structures.
Good to have: HTML, CSS.
"""

resume_paths = [
    "sample_resumes/Resume_deepesh.docx"
]

ranked = rank_candidates(jd_text, resume_paths)

print("\n✅ Ranked Candidates (Multi-Factor Scoring):\n")

for r in ranked:
    print(f"Candidate: {r.get('candidate_name')}")
    print(f"Final Score: {r.get('final_score')}")
    print(f"Similarity Score: {r.get('similarity_score')}")
    print(f"Skill Score: {r.get('skill_score')}")
    print(f"Experience Score: {r.get('experience_score')}")
    print(f"Remarks: {r.get('remarks')}")
    print(f"Matched Keywords: {r.get('matched_keywords')}")
    print(f"Missing Keywords: {r.get('missing_keywords')}")
    print("-" * 60)
