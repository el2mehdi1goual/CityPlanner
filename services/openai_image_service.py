"""
Service for generating images using OpenAI API
"""
import os
import logging
import requests
from io import BytesIO
from PIL import Image

logger = logging.getLogger(__name__)


def get_openai_api_key() -> str:
    """
    Retrieve OPENAI_API_KEY from environment variables
    
    Returns:
        str: OpenAI API key
    
    Raises:
        RuntimeError: If OPENAI_API_KEY is not set
    """
    api_key = (os.getenv("OPENAI_API_KEY", "") or "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in environment variables")
    return api_key


def enhance_prompt_with_gpt4(prompt: str) -> str:
    """
    Enhance the image prompt using GPT-4 for better image generation results
    
    Uses a professional urban planning masterplan structure to guide GPT-4
    in creating detailed, high-quality prompts for DALL-E 3.
    
    Args:
        prompt (str): Original image prompt
    
    Returns:
        str: Enhanced prompt optimized for DALL-E 3
    
    Raises:
        Exception: If GPT-4 call fails
    """
    try:
        from openai import OpenAI
        
        api_key = get_openai_api_key()
        client = OpenAI(api_key=api_key)
        
        enhancement_instruction = """You are an expert urban planning visualization specialist. 
Your task is to transform the provided urban planning prompt into a detailed, professional aerial masterplan description.

Use this proven structure for high-quality urban planning renderings:
- Start with "A professional top-down orthographic aerial masterplan of..."
- Describe the residential layout (housing types, density, architectural style)
- Include central amenities (market square, schools, health centers)
- Detail infrastructure hierarchy (boulevards, streets, pedestrian zones, parking)
- Specify green spaces percentage and landscaping elements
- Include technical details (lighting, color palette, rendering style)
- Emphasize professional, clean, high-clarity diagram quality
- Use realistic textures for materials (grass, pavement, water)
- Mention sustainable and organized design principles

Generate ONLY the enhanced prompt as a single detailed paragraph. 
No explanations, no markdown, no bullet points. 
Make it vivid, specific, and suitable for DALL-E 3 image generation.
Focus on creating a professional architectural rendering style masterplan."""
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": enhancement_instruction
                },
                {
                    "role": "user",
                    "content": f"Please enhance this urban planning prompt: {prompt}"
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        enhanced = response.choices[0].message.content.strip()
        logger.info(f"Prompt enhanced by GPT-4")
        return enhanced
        
    except Exception as e:
        logger.warning(f"Could not enhance prompt with GPT-4: {str(e)}, using original prompt")
        return prompt


def generate_image_from_prompt(prompt: str, output_dir: str = None) -> str:
    """
    Generate an image from a text prompt using OpenAI DALL-E 3 and save it locally
    
    The prompt is first enhanced by GPT-4 for better results.
    
    Args:
        prompt (str): Text prompt for image generation
        output_dir (str): Directory to save the generated image. If None, uses MEDIA_ROOT/generated_images/
    
    Returns:
        str: Relative path to the saved image file (e.g., 'generated_images/image_12345.png')
    
    Raises:
        RuntimeError: If OPENAI_API_KEY is missing or API call fails
        IOError: If image saving fails
    """
    
    try:
        from openai import OpenAI
        
        # Get API key
        api_key = get_openai_api_key()
        
        # Enhance the prompt with GPT-4
        enhanced_prompt = enhance_prompt_with_gpt4(prompt)
        logger.info(f"Original prompt: {prompt[:100]}...")
        logger.info(f"Enhanced prompt: {enhanced_prompt[:100]}...")
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Generate image using DALL-E 3 with enhanced prompt
        response = client.images.generate(
            model="dall-e-3",
            prompt=enhanced_prompt,
            size="1024x1024",
            quality="hd",
            n=1
        )
        
        # Get the image URL from the response
        image_url = response.data[0].url
        
        # Download the image from URL
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # Open image from bytes
        image = Image.open(BytesIO(image_response.content))
        
        # Prepare output directory
        if output_dir is None:
            # Use Django MEDIA_ROOT/generated_images/
            from django.conf import settings
            output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_images')
        
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate unique filename with timestamp
        import time
        timestamp = int(time.time() * 1000)
        filename = f"image_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        
        # Save image
        image.save(filepath, 'PNG')
        
        # Return relative path for Django ImageField
        relative_path = os.path.join('generated_images', filename)
        
        logger.info(f"Image generated successfully with OpenAI DALL-E 3: {relative_path}")
        return relative_path
        
    except RuntimeError as e:
        logger.error(f"OpenAI API configuration error: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"Error generating image from prompt: {str(e)}")
        raise RuntimeError(f"Failed to generate image: {str(e)}")
