import streamlit as st
import pandas as pd
import plotly.express as px
import os

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

st.divider()

if os.path.exists("outputs/submission.csv"):

    df = pd.read_csv("outputs/submission.csv")

    top_candidate = df.iloc[0]

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
            len(df[df["score"] > 0.60])
        )

    with col5:
        st.metric(
            "🥇 Best Candidate",
            top_candidate["candidate_id"][-4:]
        )

    st.divider()

    st.subheader("🏆 Top Candidates")

    display_df = df.head(20).copy()

    display_df.insert(
        0,
        "🏅 Rank",
        range(1,len(display_df)+1)
    )

    st.dataframe(
        display_df,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Results",
        df.to_csv(index=False),
        "submission.csv",
        "text/csv"
    )