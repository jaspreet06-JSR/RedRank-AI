import json

from src.semantic_match import semantic_score

job_text = """
Senior AI Engineer

Embeddings
Retrieval
Ranking
Vector Database
Python
Production ML
"""

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:

    for i, line in enumerate(f):

        candidate = json.loads(line)

        candidate_text = (
            candidate["profile"]["summary"]
            + " "
            + candidate["profile"]["headline"]
        )

        score = semantic_score(
            job_text,
            candidate_text
        )

        print(
            candidate["candidate_id"],
            round(score, 4)
        )

        if i == 9:
            break