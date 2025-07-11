from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from .auth import authenticate_user
from .db import insert_log, init_db

# 🌱 Initialize FastAPI and SQLite
app = FastAPI()
init_db()

# 🔐 Load .env and set OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📦 Pydantic model for query request
class QueryRequest(BaseModel):
    question: str
    context: str  # e.g., "Soil Moisture 45%, Temperature 33°C"
    user_id: str
    token: str

# 🚜 Farming advisory route
@app.post("/query")
def get_advice(request: QueryRequest):
    # ✅ Basic token-based authentication
    if not authenticate_user(request.user_id, request.token):
        return {"error": "Unauthorized"}

    # 🧠 Construct GPT prompt
    prompt = (
        "You are AgriGuru, an intelligent agricultural assistant.\n"
        f"Sensor Readings: {request.context}\n"
        f"Farmer's Question: {request.question}\n\n"
        "Answer in simple terms farmers can understand."
    )

    try:
        # 🔥 GPT-3.5 Turbo response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        answer = response.choices[0].message.content.strip()

        # 📝 Store in logs DB
        insert_log(request.user_id, request.question, answer)

        return {"answer": answer}

    except Exception as e:
        return {"error": f"OpenAI API failed: {str(e)}"}
