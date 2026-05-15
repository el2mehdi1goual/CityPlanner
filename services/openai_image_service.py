"""
Service for generating images using OpenAI API
"""
import os
import logging
import requests
import base64
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


def get_openai_image_model() -> str:
    """
    Get the OpenAI image model from environment or use default.
    
    Returns:
        str: Model name (default: 'gpt-image-2', fallback: 'gpt-image-1')
    """
    model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2").strip()
    if not model:
        model = "gpt-image-2"
    return model


def enhance_prompt_with_gpt4(prompt: str) -> str:
    """
    Enhance the image prompt using GPT-4 for better image generation results
    
    Uses a professional urban planning masterplan structure to guide GPT-4
    in creating detailed, high-quality prompts for OpenAI image generation.
    
    Args:
        prompt (str): Original image prompt
    
    Returns:
        str: Enhanced prompt optimized for OpenAI image generation (gpt-image-2 or gpt-image-1)
    
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
Make it vivid, specific, and suitable for OpenAI image generation.
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
    Generate an image from a text prompt using OpenAI and save it locally
    
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
        
        # Get the image model from environment
        primary_model = get_openai_image_model()
        fallback_model = "gpt-image-1"
        
        # Try primary model, fallback to gpt-image-1 if it fails
        models_to_try = [primary_model, fallback_model] if primary_model != fallback_model else [primary_model]
        
        image = None
        last_error = None
        
        for model in models_to_try:
            try:
                logger.info(f"Attempting image generation with model: {model}")
                
                # Generate image using the selected model with enhanced prompt
                # Note: gpt-image-2 and gpt-image-1 do not support response_format parameter
                # but automatically return base64 data in response.data[0].b64_json
                response = client.images.generate(
                    model=model,
                    prompt=enhanced_prompt,
                    size="1024x1024",
                    quality="medium",
                    n=1
                )
                
                logger.info(f"OpenAI API response received from {model}. Response format: {type(response.data[0])}")
                logger.info(f"Response data fields: {dir(response.data[0])}")
                
                # Handle base64 image data from response
                if hasattr(response.data[0], 'b64_json') and response.data[0].b64_json:
                    logger.info("Decoding base64 image data from OpenAI API response")
                    try:
                        # Decode base64 data
                        image_data = base64.b64decode(response.data[0].b64_json)
                        image = Image.open(BytesIO(image_data))
                        logger.info(f"Successfully decoded base64 image data from API response using model {model}")
                        break  # Success, exit the retry loop
                    except Exception as e:
                        logger.error(f"Failed to decode base64 image: {str(e)}")
                        last_error = f"Could not decode image data: {str(e)}"
                        continue
                
                # Fallback: if response contains URL (legacy format), download it
                elif hasattr(response.data[0], 'url') and response.data[0].url:
                    logger.info("Using URL-based image retrieval (legacy API response format)")
                    image_url = response.data[0].url
                    image_response = requests.get(image_url)
                    image_response.raise_for_status()
                    image = Image.open(BytesIO(image_response.content))
                    logger.info(f"Successfully retrieved image from URL using model {model}")
                    break  # Success, exit the retry loop
                
                else:
                    # Neither base64 nor URL found in response
                    logger.warning(f"No image data found in OpenAI response from model {model}")
                    last_error = "OpenAI response does not contain image data (neither b64_json nor url found)"
                    continue
                    
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"Model {model} failed: {error_msg}")
                last_error = error_msg
                # Continue to next model
                continue
        
        # If no model succeeded, raise error
        if image is None:
            error_msg = last_error or "Failed to generate image with all available models"
            logger.error(f"Image generation failed: {error_msg}")
            raise RuntimeError(error_msg)
        
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
        
        logger.info(f"Image generated successfully with OpenAI: {relative_path}")
        return relative_path
        
    except RuntimeError as e:
        logger.error(f"OpenAI API configuration error: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"Error generating image from prompt: {str(e)}")
        raise RuntimeError(f"Failed to generate image: {str(e)}")
