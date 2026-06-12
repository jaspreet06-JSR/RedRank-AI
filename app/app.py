import streamlit as st
import pandas as pd
import subprocess
import os
import json

st.set_page_config(
    page_title="RedRank AI",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# Helper Functions
# -----------------------------

def get_candidate(candidate_id):

    with open("data/candidates.jsonl", "r") as f:

        for line in f:

            candidate = json.loads(line)

            if candidate["candidate_id"] == candidate_id:
                return candidate

    return None


# -----------------------------
# UI
# -----------------------------

st.title("🚀 RedRank AI")
st.write("AI-Powered Candidate Ranking System")

# -----------------------------
# Run Ranking
# -----------------------------

if st.button("Run Ranking"):

    with st.spinner("Ranking candidates..."):
        subprocess.run(["python", "rank.py"])

    st.success("Ranking Complete!")

# -----------------------------
# Show Results
# -----------------------------

if os.path.exists("outputs/submission.csv"):

    df = pd.read_csv("outputs/submission.csv")

    df["rank"] = range(1, len(df) + 1)

    # -----------------------------
    # Dashboard Metrics
    # -----------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Candidates",
            len(df)
        )

    with col2:
        st.metric(
            "Top Score",
            round(df["score"].max(), 4)
        )

    with col3:
        st.metric(
            "Average Score",
            round(df["score"].mean(), 4)
        )

    with col4:
        st.metric(
            "Qualified",
            len(df[df["score"] > 0.60])
        )

    # -----------------------------
    # Top Candidates
    # -----------------------------

    st.subheader("🏅 Top 10 Leaderboard")

    top10 = (
        df.sort_values(
            "score",
            ascending=False
        )
        .head(10)
    )

    st.bar_chart(
        top10.set_index("candidate_id")["score"]
    )

    st.subheader("🏆 Top Candidates")

    display_df = df[
        [
            "rank",
            "candidate_id",
            "semantic",
            "retrieval",
            "experience",
            "behavior",
            "score"
        ]
    ].head(20)

    score_columns = [
        "semantic",
        "retrieval",
        "experience",
        "behavior",
        "score"
    ]

    st.dataframe(
        display_df.style.background_gradient(
            subset=score_columns,
            cmap="Greens"
        ),
        use_container_width=True
    )

    # -----------------------------
    # Download CSV
    # -----------------------------

    st.download_button(
        label="📥 Download CSV",
        data=df.to_csv(index=False),
        file_name="submission.csv",
        mime="text/csv"
    )

    st.divider()

    # -----------------------------
    # Candidate Details
    # -----------------------------

    st.subheader("📄 Candidate Details")

    search_candidate = st.text_input(
    "🔍 Search Candidate ID"
    )
    candidate_ids = df["candidate_id"].tolist()

    if search_candidate:

        filtered = [
            c for c in candidate_ids
            if search_candidate.lower()
            in c.lower()
        ]

        if filtered:
            candidate_ids = filtered

    selected_candidate = st.selectbox(
        "Select Candidate",
        candidate_ids
    )

    candidate = get_candidate(selected_candidate)

    selected_row = df[
        df["candidate_id"] == selected_candidate
    ].iloc[0]

    if candidate:

        profile = candidate.get("profile", {})

        # -----------------------------
        # Profile
        # -----------------------------

        st.markdown("## 👤 Profile")

        st.write(
            "**Candidate ID:**",
            candidate["candidate_id"]
        )

        rank_position = int(
            selected_row["rank"]
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Overall Rank",
                f"#{rank_position}"
            )

        with col2:
            st.metric(
                "Final Score",
                round(
                    selected_row["score"],
                    4
                )
            )

        st.write(
            "**Current Title:**",
            profile.get("current_title", "N/A")
        )

        st.write(
            "**Experience:**",
            profile.get("years_of_experience", 0),
            "years"
        )

        st.write(
            "**Headline:**",
            profile.get("headline", "N/A")
        )

        st.write("**Summary:**")

        st.info(
            profile.get(
                "summary",
                "No summary available"
            )
        )

        # -----------------------------
        # Ranking Reasons
        # -----------------------------

        st.subheader("🎯 Why This Candidate Ranked")

        reasons = []

        if selected_row["semantic"] > 0.50:
            reasons.append(
                "Strong semantic similarity with job description"
            )

        if selected_row["retrieval"] > 0.50:
            reasons.append(
                "Strong retrieval / search / ranking background"
            )

        if selected_row["experience"] > 0.50:
            reasons.append(
                "Relevant professional experience"
            )

        if selected_row["behavior"] > 0.50:
            reasons.append(
                "Strong professional profile"
            )

        for reason in reasons:
            st.success(reason)

        # -----------------------------
        # Score Breakdown
        # -----------------------------

        st.subheader("📊 Score Breakdown")

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

        col1, col2 = st.columns([1, 2])

        with col1:

            st.dataframe(
                score_df.style.background_gradient(
                    subset=["Value"],
                    cmap="Greens"
                ),
                use_container_width=True
            )

        with col2:

            st.bar_chart(
                score_df.set_index("Metric")
            )

        # -----------------------------
        # Skills
        # -----------------------------

        st.markdown("## 🛠 Skills")

        skills = candidate.get("skills", [])

        if skills:

            skill_names = [
                skill.get("name", "")
                for skill in skills
            ]

            st.write(
                ", ".join(skill_names)
            )

        else:
            st.write(
                "No skills found"
            )

        # -----------------------------
        # Career History
        # -----------------------------

        st.markdown("## 💼 Career History")

        for exp in candidate.get(
            "career_history",
            []
        ):

            with st.expander(
                f"{exp.get('title', 'Unknown')} @ {exp.get('company', 'Unknown')}"
            ):

                st.write(
                    "**Industry:**",
                    exp.get(
                        "industry",
                        "N/A"
                    )
                )

                st.write(
                    exp.get(
                        "description",
                        ""
                    )
                )