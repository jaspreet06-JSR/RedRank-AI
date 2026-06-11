def consistency_score(candidate):

    title = (
        candidate["profile"]
        .get("current_title", "")
        .lower()
    )

    ai_titles = [
        "machine learning",
        "ml engineer",
        "ai engineer",
        "data scientist",
        "software engineer",
        "backend engineer",
        "data engineer",
        "cloud engineer",
        "devops engineer"
    ]

    for keyword in ai_titles:
        if keyword in title:
            return 1.0

    return 0.2