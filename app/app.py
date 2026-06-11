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

    st.subheader("Top Candidates")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False),
        file_name="submission.csv",
        mime="text/csv"
    )

    st.divider()

    st.subheader("Candidate Details")

    selected_candidate = st.selectbox(
        "Select Candidate",
        df["candidate_id"].tolist()
    )

    candidate = get_candidate(selected_candidate)

    if candidate:

        profile = candidate.get("profile", {})

        st.markdown("### Profile")

        st.write(
            "**Candidate ID:**",
            candidate["candidate_id"]
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

        st.write(
            "**Summary:**"
        )

        st.info(
            profile.get("summary", "No summary available")
        )

        # Skills

        st.markdown("### Skills")

        skills = candidate.get("skills", [])

        if skills:

            skill_names = [
                skill.get("name", "")
                for skill in skills
            ]

            st.write(", ".join(skill_names))

        else:
            st.write("No skills found")

        # Career History

        st.markdown("### Career History")

        for exp in candidate.get("career_history", []):

            with st.expander(
                f"{exp.get('title', 'Unknown')} @ {exp.get('company', 'Unknown')}"
            ):

                st.write(
                    "**Industry:**",
                    exp.get("industry", "N/A")
                )

                st.write(
                    exp.get("description", "")
                )