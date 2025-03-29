# AI Empathy Gemini Project

A project demonstrating AI empathy using the Gemini API (Google AI Studio).

## Setup

1.  Create a virtual environment: `python3 -m venv .venv`
2.  Activate the virtual environment: `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows)
3.  Install dependencies: `pip install -r requirements.txt`
4.  Set your Gemini API key in `backend/config.py` (see example below)
5.  Run the backend: `uvicorn backend.main:app --reload`
6.  Run the frontend: `streamlit run frontend/app.py`

## Backend API Endpoints

- `/chat/generate_response/` - Generates an empathetic response to a user's message.

## Usage

... (Detailed instructions on how to use the API and frontend)
