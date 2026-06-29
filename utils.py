import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from packaging import version
from sklearn import __version__ as skv

# ---------------------------------------------------
# FIXED DATASET PATH
# ---------------------------------------------------
DATA_PATH = r"C:/Users/SUBITHRA/Desktop/DA1/DA/global_ai_tools_students_use.csv.xlsx"

# ---------------------------------------------------
# Load dataset
# ---------------------------------------------------
def load_dataset():
    """Loads the main AI tools dataset from fixed path."""
    try:
        df = pd.read_excel(DATA_PATH)
    except Exception as e:
        raise FileNotFoundError(f"Error loading dataset: {e}")

    # Convert boolean-like text to actual bools
    bool_cols = [c for c in df.columns if c.startswith("uses_")]
    for col in bool_cols:
        df[col] = df[col].astype(str).str.lower().map(
            {"true": True, "false": False, "yes": True, "no": False}
        )
        df[col] = df[col].fillna(False)

    # Ensure numerical usefulness columns
    rating_cols = [c for c in df.columns if c.startswith("usefulness_")]
    for col in rating_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Total_Tools_Used"] = df[bool_cols].sum(axis=1)
    return df


# ---------------------------------------------------
# OneHotEncoder helper (Sklearn 1.2+ compatibility)
# ---------------------------------------------------
def make_ohe():
    if version.parse(skv) >= version.parse("1.2"):
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    return OneHotEncoder(handle_unknown="ignore", sparse=False)


# ---------------------------------------------------
# Build Preprocessor
# ---------------------------------------------------
def build_preprocessor(df, features):
    numeric = [c for c in features if df[c].dtype != "object"]
    categorical = [c for c in features if df[c].dtype == "object"]

    ohe = make_ohe()

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric),
            ("cat", ohe, categorical)
        ],
        remainder="drop"
    )
    return preprocessor


# ---------------------------------------------------
# PCA Reduction
# ---------------------------------------------------
def run_pca(df, cols, n_components=2):
    pca = PCA(n_components=n_components, random_state=42)
    pcs = pca.fit_transform(df[cols])
    return pca, pcs


# ---------------------------------------------------
# KMeans Clustering
# ---------------------------------------------------
def run_kmeans(df, cols, k=3):
    km = KMeans(n_clusters=k, random_state=42)
    labels = km.fit_predict(df[cols])
    return km, labels


# ---------------------------------------------------
# Model Training Helper
# ---------------------------------------------------
def train_model(X, y, df, features, model_type="rf"):
    """
    model_type options:
    - "rf": Random Forest
    - "clf": Custom classifier
    """
    preprocessor = build_preprocessor(df, features)

    if model_type == "rf":
        clf = RandomForestClassifier(n_estimators=250, random_state=42)
    else:
        clf = RandomForestClassifier(random_state=42)

    pipe = Pipeline([
        ("prep", preprocessor),
        ("clf", clf)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe.fit(X_train, y_train)

    preds = pipe.predict(X_test)
    probs = pipe.predict_proba(X_test)[:, 1] if len(np.unique(y)) == 2 else None

    acc = accuracy_score(y_test, preds)
    auc = roc_auc_score(y_test, probs) if probs is not None else None

    return pipe, acc, auc


# ---------------------------------------------------
# Save model
# ---------------------------------------------------
def save_model(model, filename="model.pkl"):
    Path("model").mkdir(exist_ok=True)
    joblib.dump(model, f"model/{filename}")


# ---------------------------------------------------
# Load user test file (predictive page)
# ---------------------------------------------------
def load_test_file(uploaded_file):
    try:
        if uploaded_file.name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        return pd.read_excel(uploaded_file)
    except:
        return None


# ---------------------------------------------------
# Ranking Function (Next Tool Prediction)
# ---------------------------------------------------
def rank_tools(probabilities, tool_list):
    """
    Given a vector of probabilities for each tool,
    return a sorted ranking (highest → lowest).
    """
    ranking = sorted(
        zip(tool_list, probabilities),
        key=lambda x: x[1],
        reverse=True
    )
    return ranking


# ---------------------------------------------------
# Dependency Risk Calculator
# ---------------------------------------------------
def calculate_dependency_score(df):
    """
    Simple composite risk equation:
    dependency_score = avg_usefulness * (Total_Tools_Used / max_tools)
    """
    rating_cols = [c for c in df.columns if c.startswith("usefulness_")]
    max_tools = len([c for c in df.columns if c.startswith("uses_")])
    df["avg_rating"] = df[rating_cols].mean(axis=1)
    df["dependency_score"] = df["avg_rating"] * (df["Total_Tools_Used"] / max_tools)
    return df
