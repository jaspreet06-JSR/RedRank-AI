import json
import pandas as pd

file_path = "data/candidates.jsonl"

exp = []

with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        candidate = json.loads(line)
        exp.append(
            candidate["profile"]["years_of_experience"]
        )

df = pd.DataFrame(exp, columns=["experience"])

print(df.describe())