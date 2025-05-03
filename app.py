import streamlit as st
import numpy as np
import pickle

# Load the saved model, scaler, and label encoder
with open('best_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

try:
    with open('Label_encoder.pkl', 'rb') as f:
        le = pickle.load(f)
    label_encoding_used = True
except:
    label_encoding_used = False

# Features used during model training (12 features)
features = [
    'T1', 'T2', 'T3', 'T4', 
    'P1', 'P2', 'P3', 'P4',
    'G1', 'G2', 'G3', 'G4',
    'alpha'
]

# Excluding target feature during input
input_features = features

st.title("🔍 System Stability Prediction")

st.markdown(f"""
### Enter the values for the following {len(input_features)} features :
Paste your values in the exact order below:

`{', '.join(input_features)}`
""")

# Collect input values in separate fields for each feature
user_input = []
for feature in input_features:
    val = st.number_input(f"{feature}:", format="%.6f")
    user_input.append(val)

if st.button("Predict Stability"):
    try:
        input_array = np.array([user_input])
        scaled_input = scaler.transform(input_array)  # Scaling input based on trained scaler

        prediction = model.predict(scaled_input)[0]
        probabilities = model.predict_proba(scaled_input)[0] if hasattr(model, "predict_proba") else None

        # Decode label if label encoding was used
        if label_encoding_used:
            predicted_label = le.inverse_transform([prediction])[0]
        else:
            predicted_label = prediction

        st.success(f"✅ Predicted System Stability: **{predicted_label}**")

        if probabilities is not None:
            st.write("Prediction Probabilities:")
            if label_encoding_used:
                st.json({
                    f"Class {le.inverse_transform([i])[0]}": float(prob)
                    for i, prob in enumerate(probabilities)
                })
            else:
                st.json({f"Class {i}": float(prob) for i, prob in enumerate(probabilities)})

    except Exception as e:
        st.error(f"⚠️ Error processing input: {e}")



