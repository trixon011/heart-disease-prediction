import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

# Step 1: Load the heart data
df = pd.read_csv("heart.csv")

# Step 2: Split features and answer (target)
X = df.drop("target", axis=1)
y = df["target"]
columns = X.columns.tolist()

# Step 3: List which features are which type
categorical_features = ['cp', 'restecg', 'slope', 'ca', 'thal']
numerical_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
binary_features = ['sex', 'fbs', 'exang']

# Step 4: Split into training and test data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Step 5: Preprocessing pipelines
num_pipeline = Pipeline([('scaler', StandardScaler())])
cat_pipeline = Pipeline([('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer([
    ('num', num_pipeline, numerical_features),
    ('cat', cat_pipeline, categorical_features),
    ('pass', 'passthrough', binary_features)
])

# Step 6: Full pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', XGBClassifier(eval_metric='logloss', random_state=42))
])

# Step 7: Train
pipeline.fit(X_train, y_train)

# Step 8: Save trained pipeline
joblib.dump(pipeline, "pipeline.pkl")

# Step 9: Prediction function using probability and threshold
def predict(input_list):
    pipeline = joblib.load("pipeline.pkl")

    # Define the expected order of columns
    expected_order = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                      'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

    # Map input values based on frontend order
    frontend_order = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 
                      'sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']

    data_dict = dict(zip(frontend_order, input_list))
    reordered_input = [data_dict[col] for col in expected_order]

    # DEBUG: print reordered inputs
    print("[DEBUG] Reordered input list:", reordered_input)

    input_df = pd.DataFrame([reordered_input], columns=expected_order)

    proba = pipeline.predict_proba(input_df)[0][1]
    print(f"[DEBUG] Predicted probability of disease: {proba}")

    threshold = 0.5
    risk = "High Risk" if proba >= threshold else "Low Risk"

    return {
        "risk": risk,
        "probability": float(round(proba, 3))
    }
