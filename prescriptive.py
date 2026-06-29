import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_dataset

# ---------------------------------------------------
# PRESCRIPTIVE ANALYTICS PAGE
# ---------------------------------------------------
def prescriptive_page():

    st.title(" Prescriptive & Decisive Analytics")
    st.markdown("""
    This module provides **recommended actions**, **strategies**, and **prescriptive insights**
    based on diagnostic and predictive patterns.
    """)

    df = load_dataset()

    # -----------------------------------------
    # 1. Identify major problems
    # -----------------------------------------
    st.subheader("Key Problems Identified From Data")

    df["Total_Usefulness"] = df[[c for c in df.columns if c.startswith("usefulness_")]].mean(axis=1)
    df["Total_Usage"] = df[[c for c in df.columns if c.startswith("uses_")]].sum(axis=1)

    # Problem 1 — low usefulness
    low_rating = df[df["Total_Usefulness"] < 3]

    st.markdown("###  Problem 1 — Many students use tools but rate them poorly")
    st.write(f"Number of affected students: **{len(low_rating)}**")

    # Problem 2 — adoption gap by country
    usage_by_country = df.groupby("country")["Total_Usage"].mean().reset_index()
    low_adopt = usage_by_country[usage_by_country["Total_Usage"] < 3]

    st.markdown("###  Problem 2 — Low adoption in certain countries")
    st.dataframe(low_adopt, use_container_width=True)

    # Problem 3 — demographic differences
    usage_by_gender = df.groupby("gender")["Total_Usage"].mean().reset_index()

    st.markdown("###  Problem 3 — Gender differences in AI usage")
    st.dataframe(usage_by_gender, use_container_width=True)

    # -----------------------------------------
    # 2. Visual: Usefulness vs Usage
    # -----------------------------------------
    st.subheader(" PowerBI Style Chart — Usefulness vs Usage")

    fig_uv = px.scatter(
        df,
        x="Total_Usefulness",
        y="Total_Usage",
        color="Total_Usefulness",
        color_continuous_scale="Blues",
        title="Usefulness vs Usage Clusters",
        size_max=10
    )
    st.plotly_chart(fig_uv, use_container_width=True)

    st.markdown("""
    **Interpretation:**
    - Top-right → Satisfied heavy users  
    - Bottom-left → Students need support or training  
    - Top-left → Useful tools but low usage → awareness needed  
    """)

    # -----------------------------------------
    # 3. Prescriptive Recommendations
    # -----------------------------------------
    st.subheader(" AI-Driven Prescriptions")

    st.markdown("###  Recommended Actions")

    # Strategy lists (used in download file)
    problems = [
        "Heavy tool usage but low usefulness among many students",
        "Low AI adoption in specific countries",
        "Differences in AI tool usage across gender and grade levels"
    ]

    actions = [
        "Improve tutorials and hands-on learning for low-rated tools",
        "Launch AI awareness workshops in low-adoption countries",
        "Provide equal access and training support across all demographics",
        "Promote highly useful tools and phase out low-value tools"
    ]

    # Display the strategies nicely
    st.markdown("""
    #### ✔ Improve Tool Satisfaction
    - Provide better tutorials  
    - Collect feedback from low-rating users  
    - Introduce free premium trials  

    #### ✔ Boost AI Adoption in Low-Usage Countries
    - Add regional language support  
    - Conduct AI awareness sessions  
    - Partner with institutions  

    #### ✔ Reduce Demographic Usage Gaps
    - Tailored training for underperforming groups  
    - Equal access to AI study tools  

    #### ✔ Optimize Tool Portfolio
    - Promote top-performing tools  
    - Remove redundant or low-rated tools  
    """)

    # -----------------------------------------
    # 4. Strategy Builder
    # -----------------------------------------
    st.subheader("Strategy Builder")

    goal = st.selectbox(
        "Choose your improvement goal:",
        ["Increase Tool Adoption", "Improve Satisfaction", "Optimize Tool Portfolio"]
    )

    if goal == "Increase Tool Adoption":
        st.success("""
        **Adoption Strategy**
        - Target countries/grades with low usage  
        - Provide beginner-friendly AI workshops  
        - Introduce reward-based AI learning programs  
        """)
    elif goal == "Improve Satisfaction":
        st.success("""
        **Satisfaction Strategy**
        - Improve tool explanations  
        - Provide step-by-step guides  
        - Reduce complexity of confusing tools  
        """)
    else:
        st.success("""
        **Tool Optimization Strategy**
        - Promote tools with high usefulness  
        - Remove or improve low-rated tools  
        - Improve training where needed  
        """)

    # -----------------------------------------
    # 5. Downloadable Recommendation Report (FIXED)
    # -----------------------------------------
    st.subheader("Download Prescriptive Report")

    # Fix: pad lists so lengths match
    max_len = max(len(problems), len(actions))
    problems_padded = problems + [""] * (max_len - len(problems))
    actions_padded = actions + [""] * (max_len - len(actions))

    report_df = pd.DataFrame({
        "Problems Identified": problems_padded,
        "Recommended Actions": actions_padded
    })

    st.download_button(
        "Download Prescriptive Report (CSV)",
        report_df.to_csv(index=False).encode("utf-8"),
        "prescriptive_report.csv",
        "text/csv"
    )
