from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from app.routes.auth_routes import auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Core API Running 🚀"}


# auth routes
app.include_router(auth_router, prefix="/api/auth")
