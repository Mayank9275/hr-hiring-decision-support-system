# HR-Hiring-Decision-Support-System
## Integration Contract

### NLP/ML Module
- Input: Resume text (string)
- Output: JSON object

Example output:
{
  "score": 75,
  "decision": "Shortlisted"
}

### Backend Responsibilities
- Send resume text to NLP module
- Receive score and decision
- Expose API to frontend

### Frontend Responsibilities
- Upload resume
- Call backend API
- Display score and decision
