import json
from src.retrieval_score import retrieval_score

candidate_id = "CAND_0000862"

with open("data/candidates.jsonl", "r") as f:
    for line in f:
        candidate = json.loads(line)

        if candidate["candidate_id"] == candidate_id:

            print("TITLE:")
            print(candidate["profile"]["current_title"])

            print("\nSKILLS:")
            for skill in candidate["skills"]:
                print(skill["name"])

            print("\nRETRIEVAL:")
            print(retrieval_score(candidate))

            break