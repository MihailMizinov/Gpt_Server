from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from g4f.client import Client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "API is running"}

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "mobile_user"

client = Client()
from fastapi import Request

@app.post("/chat")
async def chat_handler(request: Request):
    body = await request.body()
    print("RAW BODY:", body)

    request_json = await request.json()
    print("JSON:", request_json)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": request_json.get("message", "")}],
            web_search=False,
            stream=False
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        print("Ошибка при вызове g4f:", e)
        raise HTTPException(status_code=500, detail=str(e))
