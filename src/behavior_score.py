def behavior_score(candidate):

    signals = candidate["redrob_signals"]

    score = 0

    github = signals.get(
        "github_activity_score", 0
    )

    interview = signals.get(
        "interview_completion_rate", 0
    )

    response = signals.get(
        "recruiter_response_rate", 0
    )

    open_to_work = signals.get(
        "open_to_work", False
    )

    score += min(github / 10, 1.0) * 0.4
    score += interview * 0.3
    score += response * 0.2

    if open_to_work:
        score += 0.1

    return min(score, 1.0)