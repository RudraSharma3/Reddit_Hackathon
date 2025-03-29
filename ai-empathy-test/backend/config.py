import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DEBUG = True

if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found. Set the GEMINI_API_KEY environment variable.")