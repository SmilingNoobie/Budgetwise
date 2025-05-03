# components/sentiment.py

from transformers import pipeline

# This model predicts 1–5 star; we map to -1…+1
sentiment_pipe = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def sentiment_score(text: str) -> float:
    """
    Returns continuous sentiment in [-1,1].
    1 star → -1.0; 3 stars → 0.0; 5 stars → +1.0
    """
    out = sentiment_pipe(text[:512])[0]  # truncate after 512 chars
    label = out["label"]    # e.g. "4 stars"
    stars = int(label.split()[0])
    return (stars - 3) / 2.0  # maps 1→-1, 3→0, 5→+1

def aggregate_scores(headlines: list[str]) -> float:
    if not headlines:
        return 0.0
    scores = [sentiment_score(h) for h in headlines]
    return sum(scores) / len(scores)
