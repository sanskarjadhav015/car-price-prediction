import streamlit as st
import pandas as pd
import pickle

# -------------------------------
# Load trained model pipeline
# -------------------------------
with open("pipeline.pkl", "rb") as f:
    model_pipeline = pickle.load(f)

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="centered"
)

# -------------------------------
# Custom CSS
# -------------------------------
st.markdown("""
<style>
/* App background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Header */
.app-header {
    text-align: center;
    padding: 25px 10px 10px 10px;
}

.app-header h1 {
    font-size: 42px;
    margin-bottom: 5px;
}

.app-header p {
    font-size: 16px;
    color: #d1d1d1;
}

/* Glass card */
.glass-card {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    padding: 30px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
}

/* Button */
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #ff512f, #dd2476);
    color: white;
    border: none;
    padding: 12px;
    font-size: 16px;
    border-radius: 12px;
    transition: 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #dd2476, #ff512f);
}

/* Footer links */
.footer {
    text-align: center;
    margin-top: 30px;
    font-size: 14px;
}

.footer a {
    color: #00ffcc;
    text-decoration: none;
    margin: 0 10px;
    font-weight: 600;
}

.footer a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header (FIXED)
# -------------------------------
st.markdown("""
<div class="app-header">
    <h1>🚗 Car Price Prediction</h1>
    <p>AI-powered resale price estimation using Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# Main Card
# -------------------------------
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

year = st.number_input("Year of Purchase", min_value=1990, max_value=2026, value=2018)
kilometers_driven = st.number_input("Kilometers Driven", min_value=0, value=40000)

fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
owner_type = st.selectbox("Owner Type", ["First", "Second", "Third", "Fourth & Above"])

seats = st.number_input("Number of Seats", min_value=2, max_value=10, value=5)
mileage = st.number_input("Mileage (km/l)", min_value=0.0, value=18.0)
engine = st.number_input("Engine (CC)", min_value=500, value=1200)
power = st.number_input("Power (bhp)", min_value=20.0, value=80.0)

if st.button("🔮 Predict Car Price"):
    input_data = pd.DataFrame({
        "Year": [year],
        "Kilometers_Driven": [kilometers_driven],
        "Fuel_Type": [fuel_type],
        "Transmission": [transmission],
        "Owner_Type": [owner_type],
        "Seats": [seats],
        "Mileage": [mileage],
        "Engine": [engine],
        "Power": [power]
    })

    prediction = model_pipeline.predict(input_data)[0]

    st.markdown(
        f"<h2 style='text-align:center; color:#00ffcc;'>💰 ₹ {prediction:,.2f}</h2>",
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# Footer / Portfolio Links
# -------------------------------
st.markdown("""
<div style="
    background-color:#0f172a;
    padding:20px;
    border-radius:14px;
    text-align:center;
">
    <p>Developed by <b>Sanskar Jadhav</b></p>
    <p>
        <a href="https://mern-portfolio-dun.vercel.app/" target="_blank">🌐 Portfolio</a> |
        <a href="https://github.com/sanskarjadhav015" target="_blank">💻 GitHub</a> |
        <a href="https://www.linkedin.com/in/jadhav-sanskar-kishor" target="_blank">🔗 LinkedIn</a> |
        <a href="mailto:sanskarjadhav015@gmail.com">✉ Email</a>
    </p>
</div>
""", unsafe_allow_html=True)
