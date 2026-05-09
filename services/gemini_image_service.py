# services/gemini_image_service.py
import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_image_from_prompt(prompt: str):
    response = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=prompt,
    )
    return response