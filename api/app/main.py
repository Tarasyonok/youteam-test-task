from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.users.router import auth_router, users_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
