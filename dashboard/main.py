"""
main.py

FastAPI application entrypoint.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_router import router


app = FastAPI(
    title="MetricMind Backend",
    version="1.0.0",
)


# Frontend origins allowed to communicate with the FastAPI backend.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",

    "http://localhost:3001",
    "http://127.0.0.1:3001",

    "http://localhost:3002",
    "http://127.0.0.1:3002",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "MetricMind backend is running.",
    }