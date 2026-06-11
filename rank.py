import json

from src.load_job import load_job_description
from src.feature_engineering import build_candidate_text
from src.semantic_match import semantic_score
from src.consistency import consistency_score
from src.experience import experience_score
from src.retrieval_score import retrieval_score
from src.behavior_score import behavior_score
from src.title_score import title_score
from src.explanation_generator import generate_explanation

job_text = load_job_description()

results = []

with open(
    "data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for i, line in enumerate(f):

        candidate = json.loads(line)

        candidate_text = build_candidate_text(
            candidate
        )

        semantic = semantic_score(
            job_text,
            candidate_text
        )

        consistency = consistency_score(
            candidate
        )

        experience = experience_score(
            candidate
        )

        retrieval = retrieval_score(
            candidate
        )

        behavior = behavior_score(
            candidate
        )

        explanation = generate_explanation(
            candidate,
            retrieval,
            behavior
        )

        title = title_score(candidate)
        score = (
            semantic * 0.35
            + consistency * 0.15
            + experience * 0.10
            + retrieval * 0.30
            + behavior * 0.10
            + title * 0.05
        )

        results.append({
            "candidate_id": candidate["candidate_id"],
            "title": candidate["profile"]["current_title"],
            "years": candidate["profile"].get("years_of_experience", 0),
            "score": round(score, 4),
            "retrieval": round(retrieval, 2),
            "explanation": explanation,
            "behavior": round(behavior, 2),
            "title": round(title, 2)
        })

        if i == 999:
            break

results.sort(
    key=lambda x: x["score"],
    reverse=True
)
for candidate in results[:5]:
    print(candidate["candidate_id"],
          "|",
          candidate["title"],
          '|',
          candidate["score"]
    )

print("\nTOP 20 CANDIDATES\n")

for r in results[:5]:

    print("\n====================")

    print("ID:", r["candidate_id"])
    print("Score:", r["score"])

    print("Reasons:")

    for reason in r["explanation"]:
        print("-", reason)