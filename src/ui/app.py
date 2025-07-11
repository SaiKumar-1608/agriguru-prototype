import streamlit as st
import requests
import sqlite3

st.title("AgriGuru: Smart Farming Assistant")

soil = st.slider("Soil Moisture", 0, 100, 50)
temp = st.slider("Temperature (°C)", 0, 50, 30)

query = st.text_input("Ask your farming question")
user_id = st.text_input("User ID", value="farmer1")
token = st.text_input("Auth Token", value="token123")

if st.button("Get Advice"):
    context = f"Current conditions: Soil Moisture {soil}%, Temperature {temp}°C"
    payload = {
        "question": query,
        "context": context,
        "user_id": user_id,
        "token": token
    }
    res = requests.post("http://localhost:8000/query", json=payload)
    if res.status_code == 200:
        result = res.json()
        if "answer" in result:
            st.success(f"Answer: {result['answer']}")
        elif "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.warning("Unexpected response from server.")

    else:
        st.error("Authentication failed or API error.")

# View user logs
if st.checkbox("Show My Past Questions"):
    conn = sqlite3.connect("src/api/logs.db")
    cur = conn.cursor()
    cur.execute("SELECT question, answer, timestamp FROM logs WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    rows = cur.fetchall()
    for q, a, ts in rows:
        st.markdown(f"**{ts}**\n- Q: {q}\n- A: {a}\n")