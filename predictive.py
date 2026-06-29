import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from utils import load_dataset

# ---------------------------------------------------
# PREDICTIVE ANALYTICS PAGE
# ---------------------------------------------------
def predictive_page():

    st.title(" Predictive Analytics")
    st.markdown("Build and evaluate a machine learning model to predict **AI Tool Adoption**.")

    # Load original dataset (no uploading)
    df = load_dataset()

    # ---------------------------------------------------
    # TARGET SELECTION
    # ---------------------------------------------------
    st.subheader(" Select Prediction Target")

    prediction_targets = [col for col in df.columns if col.startswith("uses_")]
    target = st.selectbox("Select tool to predict:", prediction_targets)

    # Define features
    rating_cols = [c for c in df.columns if c.startswith("usefulness_")]
    demo_cols = ["gender", "country", "grade", "age"]
    feature_cols = rating_cols + demo_cols

    X = df[feature_cols]
    y = df[target].astype(int)

    numeric_cols = ["age"] + rating_cols
    categorical_cols = ["gender", "country", "grade"]

    # ---------------------------------------------------
    # PREPROCESSOR
    # ---------------------------------------------------
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols)
        ]
    )

    # ---------------------------------------------------
    # RANDOM FOREST MODEL
    # ---------------------------------------------------
    model = Pipeline(
        steps=[
            ("prep", preprocessor),
            ("clf", RandomForestClassifier(n_estimators=200, random_state=42))
        ]
    )

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    # Train model
    model.fit(X_train, y_train)

    # Accuracy
    accuracy = model.score(X_test, y_test)

    st.subheader(" Model Performance")
    st.info(f"**Accuracy of the model:** `{accuracy*100:.2f}%`")

    # ---------------------------------------------------
    # Feature Importance
    # ---------------------------------------------------
    st.subheader(" Feature Importance")

    # Extract feature names after encoding
    encoded_cat = model.named_steps["prep"].named_transformers_["cat"] \
                        .get_feature_names_out(categorical_cols)
    final_features = numeric_cols + list(encoded_cat)

    importances = model.named_steps["clf"].feature_importances_

    imp_df = pd.DataFrame({
        "Feature": final_features,
        "Importance": importances
    }).sort_values("Importance", ascending=False)

    fig_imp = px.bar(
        imp_df.head(15),
        x="Feature",
        y="Importance",
        title="Top Feature Importances",
        color="Importance",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_imp, use_container_width=True)

    # ---------------------------------------------------
    # SAVE MODEL
    # ---------------------------------------------------
    model_filename = f"model_{target}.pkl"
    joblib.dump(model, model_filename)

    st.success(f"Model saved as **{model_filename}**")

    # ---------------------------------------------------
    # PREDICTION USING USER TEST FILE
    # ---------------------------------------------------
    st.subheader(" Upload Test File for Prediction")
    st.markdown("Upload **only the test dataset** containing the same columns as `feature_cols`.")

    test_file = st.file_uploader("Upload your test CSV/XLSX file", type=["csv", "xlsx"])

    if test_file:
        try:
            if test_file.name.endswith(".csv"):
                test_df = pd.read_csv(test_file)
            else:
                test_df = pd.read_excel(test_file)

            st.write("Preview of test file:", test_df.head())

            # Predict
            preds = model.predict(test_df[feature_cols])

            test_df["Prediction"] = ["WILL USE" if p == 1 else "WILL NOT USE" for p in preds]

            st.subheader(" Prediction Results")
            st.dataframe(test_df, use_container_width=True)

            # Download button
            st.download_button(
                "Download Predictions",
                test_df.to_csv(index=False).encode("utf-8"),
                "predictions.csv",
                "text/csv"
            )

        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")
