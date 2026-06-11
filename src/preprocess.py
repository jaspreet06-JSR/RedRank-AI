import json
from collections import Counter

file_path = "data/candidates.jsonl"

titles = Counter()
countries = Counter()

total_candidates = 0

with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        candidate = json.loads(line)

        total_candidates += 1

        title = candidate["profile"]["current_title"]
        country = candidate["profile"]["country"]

        titles[title] += 1
        countries[country] += 1

print(f"\nTotal Candidates: {total_candidates}")

print("\nTop 20 Titles:")
for title, count in titles.most_common(20):
    print(f"{title}: {count}")

print("\nTop Countries:")
for country, count in countries.most_common(10):
    print(f"{country}: {count}")