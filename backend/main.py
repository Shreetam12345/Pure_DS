from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv
import os

from pathlib import Path
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("CEREBRAS_API_KEY:", os.getenv("CEREBRAS_API_KEY"))  
#print("Cerebras API Key:", os.getenv("CEREBRAS_API_KEY"))

# Initialize FastAPI
app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Cerebras client (API key as environment variable)
client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))

# Input model
class NewsRequest(BaseModel):
    content: str


@app.get("/")
async def home():
    return {"message": "Backend is running!"}


@app.post("/predict")
async def predict_news(request: NewsRequest):
    text = request.content
    prompt = f"Classify this news as FAKE or REAL:\n\n{text}\n\nAnswer only 'Fake' or 'Real'."

    try:
        response = client.chat.completions.create(
            model="llama3.1-8b",
            messages=[
                {"role": "system", "content": "You are a fake news detection assistant."},
                {"role": "user", "content": prompt}
            ],
        )
        # Correct way to get the content
        result = response.choices[0].message.content
        return {"prediction": result}

    except Exception as e:
        print("🔥 Cerebras Error:", e)
        return {"prediction": f"Error connecting to Cerebras API: {e}"}

