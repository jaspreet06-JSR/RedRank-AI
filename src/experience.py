def experience_score(candidate):

    years = candidate["profile"].get(
        "years_of_experience", 0
    )

    if 5 <= years <= 9:
        return 1.0

    if 4 <= years < 5:
        return 0.8

    if 9 < years <= 12:
        return 0.8

    return 0.4