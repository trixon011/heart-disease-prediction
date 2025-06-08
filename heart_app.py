# heart_app.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;
        }
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
        }
        h1 {
            color: #d6336c;
        }
        .stButton button {
            background-color: #d6336c;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            transition: 0.3s ease;
        }
        .stButton button:hover {
            background-color: #c8235d;
        }
    </style>
""", unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("heart.csv")

# Train model
@st.cache_resource
def train_model(data):
    X = data.drop("target", axis=1)
    y = data["target"]
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

# Load data and model
df = load_data()
model = train_model(df)

# UI Start
st.markdown('<div class="main">', unsafe_allow_html=True)
st.title("💓 Heart Disease Prediction App")
st.markdown("Use this tool to predict the presence of heart disease based on patient data.")

st.markdown("### 👤 Patient Information")

# Descriptive option mappings
sex_options = {"Female": 0, "Male": 1}
cp_options = {
    "Typical Angina": 0,
    "Atypical Angina": 1,
    "Non-anginal Pain": 2,
    "Asymptomatic": 3
}
fbs_options = {
    "≤ 120 mg/dl": 0,
    "> 120 mg/dl": 1
}
restecg_options = {
    "Normal": 0,
    "ST-T Wave Abnormality": 1,
    "Left Ventricular Hypertrophy": 2
}
exang_options = {
    "No": 0,
    "Yes": 1
}
slope_options = {
    "Upsloping": 0,
    "Flat": 1,
    "Downsloping": 2
}
thal_options = {
    "Unknown": 0,
    "Normal": 1,
    "Fixed Defect": 2,
    "Reversible Defect": 3
}

# Input layout
col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Age", 29, 77, 54)
    sex = st.selectbox("Sex", list(sex_options.keys()))
    cp = st.selectbox("Chest Pain Type", list(cp_options.keys()))
    trestbps = st.slider("Resting Blood Pressure", 80, 200, 120)

with col2:
    chol = st.slider("Cholesterol", 100, 600, 245)
    fbs = st.selectbox("Fasting Blood Sugar", list(fbs_options.keys()))
    restecg = st.selectbox("Resting ECG", list(restecg_options.keys()))
    thalach = st.slider("Max Heart Rate Achieved", 70, 210, 150)

with col3:
    exang = st.selectbox("Exercise Induced Angina", list(exang_options.keys()))
    oldpeak = st.slider("ST Depression", 0.0, 6.2, 1.0)
    slope = st.selectbox("Slope of ST Segment", list(slope_options.keys()))
    ca = st.selectbox("Number of Major Vessels Colored", [0, 1, 2, 3, 4])
    thal = st.selectbox("Thalassemia", list(thal_options.keys()))

# Map inputs to numerical values
sex_val = sex_options[sex]
cp_val = cp_options[cp]
fbs_val = fbs_options[fbs]
restecg_val = restecg_options[restecg]
exang_val = exang_options[exang]
slope_val = slope_options[slope]
thal_val = thal_options[thal]

# Prediction section
st.markdown("---")
if st.button("🧠 Predict Heart Disease"):
    input_data = np.array([[age, sex_val, cp_val, trestbps, chol, fbs_val,
                            restecg_val, thalach, exang_val, oldpeak,
                            slope_val, ca, thal_val]])
    prediction = model.predict(input_data)

    st.subheader("🩺 Prediction Result:")
    if prediction[0] == 1:
        st.error("⚠️ The model predicts the patient *has heart disease*.")
    else:
        st.success("✅ The model predicts the patient *does NOT have heart disease*.")

st.markdown("</div>", unsafe_allow_html=True)
