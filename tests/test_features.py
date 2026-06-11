import json

from src.feature_engineering import (
    extract_features
)

with open(
    "data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    candidate = json.loads(next(f))

features = extract_features(
    candidate
)

print(features)