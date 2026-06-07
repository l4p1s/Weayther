from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import weather

app = FastAPI(title="Weayther API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.router, prefix="/api")
