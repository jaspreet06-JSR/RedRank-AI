import streamlit as st
import pandas as pd

st.sidebar.image(
    "https://img.icons8.com/fluency/96/rocket.png",
    width=80
)

st.sidebar.markdown(
    "## RedRank AI"
)

st.set_page_config(
    page_title="RedRank AI",
    page_icon="🚀",
    layout="wide"
)

df = pd.read_csv("outputs/submission.csv")

st.title("🚀 RedRank AI")
st.markdown("### AI-Powered Talent Intelligence Platform")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Candidates",
        len(df)
    )

with col2:
    st.metric(
        "Qualified",
        len(df[df["score"] > 0.60])
    )

with col3:
    st.metric(
        "Top Score",
        round(df["score"].max(), 4)
    )

with col4:
    st.metric(
        "Average",
        round(df["score"].mean(), 4)
    )

st.divider()

st.subheader("🎯 AI Ranking Features")

c1, c2 = st.columns(2)

with c1:
    st.success("Semantic Matching")
    st.success("Retrieval Intelligence")

with c2:
    st.success("Experience Analysis")
    st.success("Behavioral Scoring")

st.divider()

st.subheader("🚀 Quick Navigation")

col1, col2 = st.columns(2)

with col1:
    st.page_link(
        "pages/1_Dashboard.py",
        label="Open Dashboard",
        icon="📊"
    )

with col2:
    st.page_link(
        "pages/2_Candidate_Profile.py",
        label="Candidate Explorer",
        icon="👤"
    )