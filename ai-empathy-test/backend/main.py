from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import gemini_chat
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Empathy Gemini API",
    description="An API for generating empathetic responses using the Gemini API.",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gemini_chat.router, prefix="/chat", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Empathy Gemini API!"}

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")
    logger.info("Application startup tasks completed.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application...")