import json

from src.feature_engineering import (
    build_candidate_text
)

with open(
    "data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    first = json.loads(next(f))

text = build_candidate_text(first)

print(text[:2000])