import re
import spacy

# Load spacy model (make sure you ran: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")


def preprocess_text(text: str) -> str:
    """
    Clean + normalize text for TF-IDF:
    - lowercase
    - remove extra spaces
    - keep only words/numbers
    - remove stopwords
    - lemmatize tokens
    """
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)   # remove special chars
    text = re.sub(r"\s+", " ", text).strip()  # remove extra spaces

    doc = nlp(text)

    tokens = []
    for token in doc:
        if token.is_stop:
            continue
        if token.is_space:
            continue
        if len(token.text.strip()) <= 2:
            continue

        tokens.append(token.lemma_)

    return " ".join(tokens)
