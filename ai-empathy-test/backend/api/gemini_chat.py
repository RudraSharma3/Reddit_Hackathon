import google.generativeai as genai
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from typing import List, Dict
from backend.config import GEMINI_API_KEY
import os
from transformers import pipeline  # Sentiment analysis

# Configure logging
logger = logging.getLogger(__name__)

# FastAPI Router
router = APIRouter()

# Configure Gemini API
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # List available models for debugging purposes.  IMPORTANT.
    for m in genai.list_models():
        logger.info(f"Available model: {m.name}")

    model_name = os.environ.get("GEMINI_MODEL_NAME", "gemini-1.5-pro-latest") #Default and configurable
    logger.info(f"Attempting to use model: {model_name}")
    model = genai.GenerativeModel(model_name)

except Exception as e:
    logger.error(f"Error configuring Gemini API: {e}")
    raise HTTPException(status_code=500, detail=f"Error configuring Gemini API: {str(e)}")


# Sentiment Analysis Pipeline (Initialize outside the function for efficiency)
try:
    sentiment_pipeline = pipeline("sentiment-analysis") # Defaults to distilbert-base-uncased
except Exception as e:
    logger.error(f"Error initializing sentiment analysis pipeline: {e}")
    sentiment_pipeline = None  # Disable it if initialization fails


# Define request model
class ChatRequest(BaseModel):
    user_message: str

    @validator("user_message")
    def validate_user_message(cls, value):
        if not value:
            raise ValueError("User message cannot be empty.")
        if len(value) > 1000:
            raise ValueError("User message exceeds maximum length (1000).")
        return value

class SentimentAnalysisResult(BaseModel):
    label: str # "POSITIVE", "NEGATIVE", "NEUTRAL"
    score: float  # Confidence score (0-1)

class ChatResponse(BaseModel):
    response: str
    sentiment: SentimentAnalysisResult  # Include sentiment data

@router.post("/generate_response/", response_model=ChatResponse)
async def generate_empathetic_response(request: ChatRequest):
    """
    Generates an empathetic response to a user's message using the Gemini API,
    incorporating sentiment analysis.
    """
    try:
        user_message = request.user_message

        # Perform Sentiment Analysis (if the pipeline is initialized)
        if sentiment_pipeline:
            sentiment_result = sentiment_pipeline(user_message)[0]  # Get the first result
            sentiment = SentimentAnalysisResult(label=sentiment_result["label"], score=sentiment_result["score"])
            logger.info(f"Sentiment analysis: {sentiment}")
        else:
            sentiment = SentimentAnalysisResult(label="NEUTRAL", score=0.5)  # Default if pipeline failed
            logger.warning("Sentiment analysis pipeline is disabled.")

        # Craft the Gemini Prompt based on Sentiment
        if sentiment.label == "NEGATIVE":
            gemini_prompt = f"""
            The user's message has a negative sentiment with a score of {sentiment.score}. Respond with a message that acknowledges their negative emotion, offers support, and encourages them to share more.
            User message: {user_message}
            """
        elif sentiment.label == "POSITIVE":
            gemini_prompt = f"""
            The user's message has a positive sentiment with a score of {sentiment.score}. Respond with a message that acknowledges their positive emotion, offers support, and encourages them to continue sharing their positive experiences.
            User message: {user_message}
            """
        else:  # Neutral
            gemini_prompt = f"""
            The user's message has a neutral sentiment with a score of {sentiment.score}. Respond with a message that shows you're listening and encourages them to share more.
            User message: {user_message}
            """

        prompt_parts = [
           """You are an empathetic AI assistant named EmpathyBot.  Your role is to listen and respond with compassion, 
            acknowledging the user's feelings and offering support.  Be concise and helpful.""" , # System prompt first
            gemini_prompt  # Then the sentiment-aware prompt
        ]


        response = model.generate_content(prompt_parts)  # Use the sentiment-aware prompt
        response_text = response.text

        if response.prompt_feedback:
          if response.prompt_feedback.block_reason:
            raise HTTPException(status_code=400, detail=f"Response was blocked because: {response.prompt_feedback.block_reason}")


        logger.info(f"Generated response: {response_text}")
        return ChatResponse(response=response_text, sentiment=sentiment)


    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")