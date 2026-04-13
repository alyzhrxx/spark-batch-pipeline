import streamlit as st
import pickle
import pandas as pd

# Load model
MODEL_PATH = "models/traffic_model.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

st.title("Smart City Traffic Prediction Dashboard")

st.subheader("Input Data")

# Input user
hour = st.slider("Hour (0-23)", 0, 23, 12)

day = st.selectbox(
    "Day of Week",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

# Convert day ke angka (sesuai model)
day_mapping = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}

day_num = day_mapping[day]

# Prediction
input_data = pd.DataFrame([[hour, day_num]], columns=["hour", "day"])

prediction = model.predict(input_data)[0]

st.subheader("Prediction Result")
st.success(f"Estimated Traffic Volume: {int(prediction)} vehicles")

st.info("This prediction is based on historical traffic patterns using Random Forest model.")
