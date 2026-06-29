import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_dataset

# ---------------------------------------------------
# DESCRIPTIVE ANALYTICS PAGE
# ---------------------------------------------------
def descriptive_page():

    st.title(" Descriptive Analytics")
    st.markdown("Analyze the structure, summary, and distribution of your dataset.")

    # Load dataset
    df = load_dataset()

    st.subheader(" Dataset Overview")
    st.write("Shape:", df.shape)
    st.dataframe(df.head(), use_container_width=True)

   

    # -------------------------
    # Summary Statistics
    # -------------------------
    st.subheader(" Summary Statistics")
    st.dataframe(df.describe(include="all"), use_container_width=True)

    # -------------------------
    # Numeric Distribution
    # -------------------------
    st.subheader(" Numeric Feature Distributions")

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    selected_num = st.selectbox("Select numeric column:", numeric_cols)

    fig_hist = px.histogram(
        df,
        x=selected_num,
        nbins=20,
        title=f"Distribution of {selected_num}",
        color_discrete_sequence=["#003366"]
    )
    st.plotly_chart(fig_hist, use_container_width=True)

   

    # -------------------------
    # Categorical distribution
    # -------------------------
    st.subheader(" Categorical Feature Distribution")

    cat_cols = df.select_dtypes(include=["object", "bool"]).columns.tolist()

    selected_cat = st.selectbox("Select categorical column:", cat_cols)

    cat_df = df[selected_cat].value_counts().reset_index()
    cat_df.columns = [selected_cat, "Count"]

    fig_cat = px.bar(
        cat_df,
        x=selected_cat,
        y="Count",
        title=f"Value counts of {selected_cat}",
        text_auto=True,
        color_discrete_sequence=["#0059b3"]
    )
    st.plotly_chart(fig_cat, use_container_width=True)

    # -------------------------
    # Correlation Heatmap
    # -------------------------
    st.subheader(" Correlation Heatmap")

    corr = df[numeric_cols].corr()

    fig_corr = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="Blues"
        )
    )

    fig_corr.update_layout(
        title="Correlation Heatmap (Numeric Features)"
    )

    st.plotly_chart(fig_corr, use_container_width=True)

    # -------------------------
    # Download summary
    # -------------------------
    st.subheader(" Download Summary Files")

    csv = df.describe(include="all").to_csv().encode("utf-8")
    st.download_button(
        "Download Summary CSV",
        csv,
        "descriptive_summary.csv",
        "text/csv",
        key="download-summary"
    )
