import streamlit as st
import pandas as pd
import plotly.express as px
import os
import subprocess

st.sidebar.title("🚀 RedRank AI")

st.markdown("""
# 🚀 RedRank AI

### AI-Powered Candidate Ranking Platform
""")

st.set_page_config(
    page_title="RedRank AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.subheader("📄 Job Description")

uploaded_jd = st.file_uploader(
    "Upload Job Description",
    type=["txt", "pdf", "docx"]
)

jd_text = ""

if uploaded_jd is not None:

    if uploaded_jd.name.endswith(".txt"):

        try:
            jd_text = uploaded_jd.read().decode("utf-8")
        except:
            jd_text = uploaded_jd.read().decode(
                "latin-1",
                errors="ignore"
            )

        st.text_area(
            "Job Description",
            jd_text,
            height=200
        )

        st.info(
            f"""
        📌 JD Loaded Successfully

        Characters: {len(jd_text)}

        Preview:
        {jd_text[:250]}...
        """
        )

if st.button("🚀 Rank Candidates"):

    if uploaded_jd is not None:

        with open(
            "data/job_description.txt",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(jd_text)

        with st.spinner(
            "Ranking candidates..."
        ):

            subprocess.run(
                ["python", "rank.py"]
            )

        st.success(
            "Ranking completed successfully"
        )

        df = pd.read_csv(
            "outputs/submission.csv"
        )

        top_candidate = df.iloc[0]

        st.markdown("## 🏆 Why Candidate Ranked #1")

        st.success(
            f"""
        Candidate: {top_candidate['candidate_id']}

        Final Score: {top_candidate['score']:.4f}
        """
        )

        st.rerun()

st.divider()

if os.path.exists("outputs/submission.csv"):

    df = pd.read_csv(
        "outputs/submission.csv"
    )

    top_candidate = df.iloc[0]

    st.markdown("## 📊 Recruitment Dashboard")

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.metric(
            "👥 Candidates",
            f"{len(df):,}"
        )

    with col2:
        st.metric(
            "🏆 Top Score",
            f"{df['score'].max():.4f}"
        )

    with col3:
        st.metric(
            "📈 Average",
            f"{df['score'].mean():.4f}"
        )

    with col4:
        st.metric(
            "✅ Qualified",
            len(
                df[
                    df["score"] > 0.60
                ]
            )
        )

    with col5:
        st.metric(
            "🥇 Best Candidate",
            top_candidate["candidate_id"][-4:]
        )

    st.divider()

    st.markdown("## 🏆 Top Candidate Insight")

    col_left,col_right = st.columns([1,1])

    with col_left:

        st.success(
            f"""
Candidate ID: {top_candidate['candidate_id']}

Final Score: {top_candidate['score']:.4f}
"""
        )

        st.markdown("### 💡 Why Ranked #1")

        if top_candidate["semantic"] > 0.5:
            st.success("Strong semantic skill match")

        if top_candidate["retrieval"] > 0.5:
            st.success("Relevant project experience")

        if top_candidate["experience"] > 0.5:
            st.success("Strong experience profile")

        if top_candidate["behavior"] > 0.5:
            st.success("Positive hiring signals")

    with col_right:

        score_df = pd.DataFrame({
            "Metric":[
                "Semantic",
                "Retrieval",
                "Experience",
                "Behavior"
            ],
            "Score":[
                top_candidate["semantic"],
                top_candidate["retrieval"],
                top_candidate["experience"],
                top_candidate["behavior"]
            ]
        })

        fig = px.bar(
            score_df,
            x="Metric",
            y="Score",
            title="Score Breakdown"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.markdown("## 🏅 Top 20 Candidates")

    leaderboard = df.head(20).copy()

    leaderboard.insert(
        0,
        "Rank",
        range(
            1,
            len(leaderboard)+1
        )
    )

    st.dataframe(
        leaderboard,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "📥 Download Ranking Results",
        df.to_csv(index=False),
        "submission.csv",
        "text/csv",
        use_container_width=True
    )