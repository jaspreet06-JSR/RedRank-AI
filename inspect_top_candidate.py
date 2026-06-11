import json

candidate_id = input(
    "Enter candidate ID to inspect: "
).strip()

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        candidate = json.loads(line)

        if candidate["candidate_id"] == candidate_id:

            print("\n===== TITLE =====")
            print(candidate["profile"]["current_title"])

            print("\n===== HEADLINE =====")
            print(candidate["profile"]["headline"])

            print("\n===== SUMMARY =====")
            print(candidate["profile"]["summary"])

            print("\n===== CAREER HISTORY =====")

            for job in candidate["career_history"]:

                print("\n------------------")
                print("Company:", job["company"])
                print("Title:", job["title"])
                print("Industry:", job["industry"])

                print("\nDescription:")
                print(job["description"])

            print("\n===== SKILLS =====")

            for skill in candidate["skills"]:
                print(
                    skill["name"],
                    "|",
                    skill["proficiency"]
                )

            break