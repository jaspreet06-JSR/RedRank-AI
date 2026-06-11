def build_candidate_text(candidate):

    text = []

    profile = candidate["profile"]

    text.append(profile.get("headline", ""))
    text.append(profile.get("summary", ""))

    for exp in candidate.get("career_history", []):
        text.append(exp.get("title", ""))
        text.append(exp.get("description", ""))

    for skill in candidate.get("skills", []):
        text.append(skill.get("name", ""))

    return " ".join(text)


def extract_features(candidate):

    profile = candidate["profile"]
    signals = candidate["redrob_signals"]

    features = {}

    features["years_exp"] = profile.get(
        "years_of_experience", 0
    )

    features["relocate"] = int(
        signals.get(
            "willing_to_relocate", False
        )
    )

    features["github_score"] = signals.get(
        "github_activity_score", 0
    )

    features["endorsements"] = signals.get(
        "endorsements_received", 0
    )

    features["interview_rate"] = signals.get(
        "interview_completion_rate", 0
    )

    features["connections"] = signals.get(
        "connection_count", 0
    )

    return features