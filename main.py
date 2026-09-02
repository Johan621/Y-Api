from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import os
from google import genai
from google.genai import types

app = FastAPI()

# Get the free Google API key from the environment
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

class DataRequest(BaseModel):
    text: str

@app.post("/extract")
async def extract_data(request: DataRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    prompt = f"Extract all names, dates, and financial figures from this text and return ONLY raw JSON:\n\n{request.text}"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return {"extracted_data": response.text}
    except Exception as e:
        return {
            "error": str(e)
        }
