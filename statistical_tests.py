import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind
from utils import load_dataset


def statistical_tests_page():

    st.title("Statistical Tests")

    df = load_dataset()

    st.subheader("Chi-Square Test of Independence")

    col1, col2 = st.columns(2)
    with col1:
        col_x = st.selectbox("Select Categorical Variable 1", df.columns)
    with col2:
        col_y = st.selectbox("Select Categorical Variable 2", df.columns)

    if st.button("Run Chi-Square Test"):
        contingency = pd.crosstab(df[col_x], df[col_y])
        chi2, p, dof, expected = chi2_contingency(contingency)

        st.write("### Contingency Table")
        st.dataframe(contingency)

        st.write(f"**Chi-Square Statistic:** {chi2:.4f}")
        st.write(f"**p-Value:** {p:.4f}")
        st.write(f"**Degrees of Freedom:** {dof}")

        if p < 0.05:
            st.success("There is a significant relationship between the variables.")
        else:
            st.info("No significant relationship found between the variables.")

    st.markdown("---")
    st.subheader("Independent Samples t-Test")

    group_col = st.selectbox("Select Grouping Column (categorical)", df.columns)
    value_col = st.selectbox("Select Numeric Value Column", df.columns)

    groups = df[group_col].unique()

    if len(groups) >= 2:
        group1 = st.selectbox("Group 1", groups)
        group2 = st.selectbox("Group 2", groups)
    else:
        st.warning("Select a column with at least 2 groups.")
        return

    if st.button("Run t-Test"):
        data1 = df[df[group_col] == group1][value_col]
        data2 = df[df[group_col] == group2][value_col]

        t_stat, p_value = ttest_ind(data1, data2, equal_var=False)

        st.write(f"**t-Statistic:** {t_stat:.4f}")
        st.write(f"**p-Value:** {p_value:.4f}")

        st.write(f"Mean of {group1}: **{data1.mean():.2f}**")
        st.write(f"Mean of {group2}: **{data2.mean():.2f}**")

        if p_value < 0.05:
            st.success("The groups have significantly different means.")
        else:
            st.info("No significant difference between the group means.")
