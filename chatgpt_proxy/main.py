from contextlib import asynccontextmanager
from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from db import Base, add_request_data, engine, get_users_requests
from gemini_client import get_answer_from_gemini

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print("Database tables created.")
    yield

app = FastAPI(
    title="ChatGPT Proxy API",
    lifespan=lifespan
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/requests")
def get_my_requests(request: Request):
    user_api_address = request.client.host
    print(f"User IP address: {user_api_address}")
    user_requests = get_users_requests(ip_address=user_api_address)
    return user_requests

@app.post("/requests")
def send_prompt(
    request: Request,
    prompt: str = Body(embed=True)
    ):
    user_api_address = request.client.host
    answer = get_answer_from_gemini(prompt)
    add_request_data(
        ip_address=user_api_address,
        prompt=prompt,
        response=answer
    )
    return {"answer": answer}

