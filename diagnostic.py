import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from utils import load_dataset

# ---------------------------------------------------
# DIAGNOSTIC ANALYTICS PAGE
# ---------------------------------------------------
def diagnostic_page():

    st.title(" Diagnostic Analytics")
    st.markdown("Identify **why** patterns occur in the dataset using PCA, clustering tendencies, and root-cause insights.")

    # Load dataset
    df = load_dataset()

    st.subheader("Dataset Overview")
    st.write("Dataset contains:", df.shape[0], "rows and", df.shape[1], "columns.")
    st.dataframe(df.head(), use_container_width=True)

    # ---------------------------------------------------
    # PCA for DIMENSIONALITY REDUCTION
    # ---------------------------------------------------
    st.subheader(" PCA Dimensionality Reduction (2D)")

    rating_cols = [c for c in df.columns if c.startswith("usefulness_")]
    usage_cols = [c for c in df.columns if c.startswith("uses_")]

    combined_features = rating_cols + usage_cols

    X = df[combined_features].astype(float)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(X_scaled)

    df["PC1"] = pca_result[:, 0]
    df["PC2"] = pca_result[:, 1]

    fig_pca = px.scatter(
        df,
        x="PC1",
        y="PC2",
        color=df[usage_cols].sum(axis=1),
        title="PCA Plot (2D) — Patterns in AI Tool Use",
        color_continuous_scale="Blues",
        labels={"color": "Total Tools Used"}
    )
    st.plotly_chart(fig_pca, use_container_width=True)

    st.markdown(f"""
    **PCA Insights:**
    - PC1 explains **{pca.explained_variance_ratio_[0]*100:.2f}%** variance  
    - PC2 explains **{pca.explained_variance_ratio_[1]*100:.2f}%** variance  
    - Students separated widely = inconsistent usage  
    - Students grouped tightly = similar usage behavior  
    """)

   
    # ---------------------------------------------------
    # Root Cause Analysis
    # ---------------------------------------------------
    st.subheader("Root Cause Analysis of AI Tool Usage")

    selected_tool = st.selectbox("Select a tool for diagnostic analysis:", usage_cols)

    root_df = df.groupby(selected_tool)[rating_cols].mean().reset_index()

    fig_root = px.bar(
        root_df,
        x=selected_tool,
        y=root_df.columns[1:],
        barmode="group",
        title=f"Average Usefulness Ratings Based on {selected_tool.upper()} Usage",
        color_discrete_sequence=px.colors.sequential.Blues
    )
    st.plotly_chart(fig_root, use_container_width=True)

    st.markdown(f"""
    **Root Cause Insight for `{selected_tool}`:**
    - If usefulness of other tools increases when `{selected_tool}` is `True`,
      then students who like `{selected_tool}` tend to be **active AI adopters**.
    - If usefulness of other tools decreases, `{selected_tool}` users may be **single-tool dominant**.
    """)

    # ---------------------------------------------------
    # Drill Down for a Selected Demographic
    # ---------------------------------------------------
    st.subheader(" Demographic Drill-Down Diagnostics")

    demo_cols = ["gender", "grade", "country"]

    selected_demo = st.selectbox("Select demographic attribute:", demo_cols)

    demo_df = df.groupby(selected_demo)[rating_cols + ["Total_Tools_Used"]].mean().reset_index()

    fig_demo = px.line(
        demo_df,
        x=selected_demo,
        y="Total_Tools_Used",
        title="AI Tool Usage by Demographic Group",
        markers=True
    )
    st.plotly_chart(fig_demo, use_container_width=True)

    st.markdown(f"""
    **Insights for `{selected_demo}`:**
    - Groups with high average usefulness often use **more AI tools**.
    - Groups with lower usefulness means need **better training or guidance**.
    """)

   