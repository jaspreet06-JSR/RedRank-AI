def title_score(candidate):

    title = candidate["profile"]["current_title"].lower()

    good_titles = [
        "ml engineer",
        "machine learning engineer",
        "ai engineer",
        "data scientist",
        "data engineer",
        "software engineer",
        "backend engineer",
        "search engineer",
        "cloud engineer"
    ]

    for t in good_titles:
        if t in title:
            return 1.0

    return 0.0