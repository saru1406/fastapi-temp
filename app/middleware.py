from fastapi.middleware.cors import CORSMiddleware
from .main import app
from dotenv import load_dotenv
import os

load_dotenv()

origins = [
    os.getenv("CORS"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
