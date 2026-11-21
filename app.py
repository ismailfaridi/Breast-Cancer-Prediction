import streamlit as st
import pandas as pd
import joblib

MODEL_PATH = "breast_cancer_prediction_logistic_regression.pkl"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# Must match the exact 5 features the model was trained on, in order
FEATURES = [
    "radius_worst",
    "concave points_worst",
    "area_worst",
    "concave points_mean",
    "perimeter_worst",
]

# Real sample rows from the dataset (for the preset buttons)
SAMPLE_MALIGNANT = {
    "radius_worst": 25.38,
    "concave points_worst": 0.2654,
    "area_worst": 2019.0,
    "concave points_mean": 0.1471,
    "perimeter_worst": 184.6,
}

SAMPLE_BENIGN = {
    "radius_worst": 11.42,
    "concave points_worst": 0.0215,
    "area_worst": 177.4,
    "concave points_mean": 0.0100,
    "perimeter_worst": 75.1,
}


# UI
st.set_page_config(page_title="Breast Cancer Prediction", page_icon="🎗️")
st.title("🎗️ Breast Cancer Prediction")
st.caption("Logistic Regression · 5 features · Wisconsin Breast Cancer Dataset")

st.markdown(
    "Adjust the values below (or load a sample patient) and click **Predict**."
)

# Session-state sliders so preset buttons can fill them
if "vals" not in st.session_state:
    st.session_state.vals = dict(SAMPLE_BENIGN)

col1, col2 = st.columns(2)
with col1:
    if st.button("Load sample: Benign"):
        st.session_state.vals = dict(SAMPLE_BENIGN)
with col2:
    if st.button("Load sample: Malignant"):
        st.session_state.vals = dict(SAMPLE_MALIGNANT)

# Sliders bound to session state
st.subheader("Patient measurements")
v = st.session_state.vals

v["radius_worst"] = st.slider("Worst Radius", 7.0, 36.0, float(v["radius_worst"]))
v["concave points_worst"] = st.slider("Worst Concave Points", 0.0, 0.30, float(v["concave points_worst"]))
v["area_worst"] = st.slider("Worst Area", 185.0, 4254.0, float(v["area_worst"]))
v["concave points_mean"] = st.slider("Mean Concave Points", 0.0, 0.20, float(v["concave points_mean"]))
v["perimeter_worst"] = st.slider("Worst Perimeter", 50.0, 251.0, float(v["perimeter_worst"]))

st.session_state.vals = v

# Predict
if st.button("🔍 Predict", type="primary"):
    input_df = pd.DataFrame([v])[FEATURES]   # enforce exact order
    proba = float(model.predict_proba(input_df)[0, 1])
    pred = int(model.predict(input_df)[0])

    st.divider()
    if pred == 1:
        st.error(f"### Prediction: **Malignant**\nProbability of malignant: **{proba:.1%}**")
    else:
        st.success(f"### Prediction: **Benign**\nProbability of malignant: **{proba:.1%}**")

    st.progress(proba)
    st.caption("Note: demonstration only — not a medical device.")