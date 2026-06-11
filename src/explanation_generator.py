def generate_explanation(candidate, retrieval, behavior):

    reasons = []

    years = candidate["profile"].get(
        "years_of_experience",
        0
    )

    if years >= 5:
        reasons.append(
            f"{years} years of relevant experience"
        )

    if retrieval >= 0.5:
        reasons.append(
            "Strong retrieval / semantic search background"
        )

    if behavior >= 0.5:
        reasons.append(
            "Strong professional signal score"
        )

    skills = [
        skill["name"]
        for skill in candidate.get("skills", [])
    ]

    important_skills = []

    for s in skills:
        s_lower = s.lower()

        if (
            "llm" in s_lower
            or "langchain" in s_lower
            or "rag" in s_lower
            or "semantic" in s_lower
            or "retrieval" in s_lower
            or "vector" in s_lower
        ):
            important_skills.append(s)

    if important_skills:
        reasons.append(
            "Relevant skills: "
            + ", ".join(important_skills[:5])
        )

    return reasons