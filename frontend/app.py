import streamlit as st
import requests

st.set_page_config(page_title="Fake News Detector", page_icon="📰")

st.title("📰 Fake News Detector")
st.write("This app will classify the entered news as *Fake* or *Real* using the Llama model (via Cerebras).")

news_text = st.text_area("Enter news article or statement:", height=200)

if st.button("Check"):
    if news_text.strip():
        with st.spinner("Analyzing..."):
            # Temporary backend URL (we'll replace later)
            backend_url = "http://127.0.0.1:8000/predict"

            try:
                response = requests.post(backend_url, json={"content": news_text})
                if response.status_code == 200:
                    result = response.json()["prediction"]
                    st.success(f"Prediction: **{result}** 🧠")
                else:
                    st.error("Error: Could not get response from backend.")
            except Exception as e:
                st.error(f"Connection error: {e}")
    else:
        st.warning("Please enter some text first.")
