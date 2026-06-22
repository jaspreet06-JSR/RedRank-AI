import streamlit as st
import pandas as pd
import json
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Candidate Profile",
    page_icon="👤",
    layout="wide"
)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.markdown("""
# 🚀 RedRank AI
### Talent Intelligence
""")

# =====================================
# LOAD CANDIDATE
# =====================================

def get_candidate(candidate_id):

    with open("data/candidates.jsonl", "r") as f:

        for line in f:

            candidate = json.loads(line)

            if candidate["candidate_id"] == candidate_id:
                return candidate

    return None


# =====================================
# LOAD RESULTS
# =====================================

df = pd.read_csv(
    "outputs/submission.csv"
)

qualified_df = (
    df.sort_values(
        "score",
        ascending=False
    )
    .head(50)
)

candidate_ids = qualified_df[
    "candidate_id"
].tolist()

# =====================================
# PAGE HEADER
# =====================================

st.title("👤 Candidate Profile")

st.caption(
    "Search and analyze ranked candidates"
)

st.write("")

# =====================================
# SEARCH
# =====================================

selected_candidate = st.selectbox(
    "🔍 Search Candidate",
    candidate_ids
)

candidate = get_candidate(
    selected_candidate
)

selected_row = qualified_df[
    qualified_df["candidate_id"]
    ==
    selected_candidate
].iloc[0]

rank_position = (
    qualified_df.index[
        qualified_df["candidate_id"]
        ==
        selected_candidate
    ][0]
    + 1
)

profile = candidate.get(
    "profile",
    {}
)

# =====================================
# KPI CARDS
# =====================================

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("🏅 Rank", f"#{rank_position}")

with k2:
    st.metric(
        "🎯 Match Score",
        f"{selected_row['score']:.4f}"
    )

with k3:
    st.metric(
        "💼 Experience",
        f"{profile.get('years_of_experience',0)} Years"
    )

with k4:
    st.metric(
        "🧠 Role",
        profile.get(
            "current_title",
            "N/A"
        )
    )

st.divider()

# =====================================
# ROW 1
# Profile + Summary
# =====================================

left1, right1 = st.columns(2)

with left1:

    st.markdown("## 👤 Profile")

    st.write(
        "**Candidate ID:**",
        candidate["candidate_id"]
    )

    st.write(
        "**Current Title:**",
        profile.get(
            "current_title",
            "N/A"
        )
    )

    st.write(
        "**Headline:**",
        profile.get(
            "headline",
            "N/A"
        )
    )

    st.write(
        "**Experience:**",
        profile.get(
            "years_of_experience",
            0
        ),
        "Years"
    )

with right1:

    st.markdown(
        "## 📝 Professional Summary"
    )

    st.info(
        profile.get(
            "summary",
            "No summary available"
        )
    )

st.divider()

# =====================================
# ROW 2
# Ranking + Chart
# =====================================

left2, right2 = st.columns(2)

with left2:

    st.markdown(
        "## 🎯 Why This Candidate Ranked"
    )

    if selected_row["semantic"] > 0.5:
        st.success(
            "Strong semantic match"
        )

    if selected_row["retrieval"] > 0.5:
        st.success(
            "Strong retrieval background"
        )

    if selected_row["experience"] > 0.5:
        st.success(
            "Relevant experience"
        )

    if selected_row["behavior"] > 0.5:
        st.success(
            "Strong professional signal"
        )

with right2:

    st.markdown(
        "## 📊 Score Breakdown"
    )

    score_df = pd.DataFrame({
        "Metric": [
            "Semantic",
            "Retrieval",
            "Experience",
            "Behavior",
            "Final Score"
        ],
        "Value": [
            selected_row["semantic"],
            selected_row["retrieval"],
            selected_row["experience"],
            selected_row["behavior"],
            selected_row["score"]
        ]
    })

    fig = px.bar(
        score_df,
        x="Metric",
        y="Value",
        color="Value"
    )

    fig.update_layout(
        showlegend=False,
        height=350
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

st.markdown("## 🛠 Skills")

skills = candidate.get("skills", [])

cols = st.columns(4)

for i, skill in enumerate(skills[:12]):

    name = (
        skill["name"]
        if isinstance(skill, dict)
        else str(skill)
    )

    with cols[i % 4]:
        st.info(name)

st.divider()

# =====================================
# FULL WIDTH CAREER HISTORY
# =====================================

st.markdown(
    "## 💼 Career History"
)

for exp in candidate.get(
    "career_history",
    []
):

    with st.expander(
        f"{exp.get('title','Unknown')} @ {exp.get('company','Unknown')}"
    ):

        st.write(
            exp.get(
                "description",
                ""
            )
        )