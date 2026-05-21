import os
from pathlib import Path

from google import genai

try:
    # Prefer an explicit search path so `.env` is found reliably on Windows.
    from decouple import AutoConfig

    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    env = AutoConfig(search_path=str(PROJECT_ROOT))
except Exception:  # pragma: no cover
    env = None


def _get_api_key() -> str:
    # Prefer process env (works with python-dotenv in Django settings),
    # then fall back to python-decouple if available.
    key = (os.getenv("GEMINI_API_KEY", "") or "").strip()
    if key:
        return key
    if env is not None:
        return (env("GEMINI_API_KEY", default="") or "").strip()
    return ""


def _get_text_model() -> str:
    model = (os.getenv("GEMINI_TEXT_MODEL", "") or "").strip()
    if model:
        return model if model.startswith("models/") else f"models/{model}"
    if env is not None:
        model = (env("GEMINI_TEXT_MODEL", default="") or "").strip()
        if model:
            return model if model.startswith("models/") else f"models/{model}"
    return "models/gemini-2.5-flash"


def generate_image_prompt_from_project(project_data: dict) -> str:
    """
    Generate a single, high-quality urban masterplan image prompt using Gemini.
    Returns prompt text only.
    """
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing. Set it in your environment or `.env`.")

    # NOTE: in CityPlanner, `surface_terrain` is in hectares.
    land_hectares = project_data.get("surface_terrain", "unknown")
    estimated_people = int(project_data.get("nombre_familles", 0)) * int(project_data.get("taille_moyenne_famille", 0))

    instruction = f"""
You are an expert urban planning visualization assistant.

Generate ONE detailed image prompt in English for an AI image generator.
The output must be a realistic, professional TOP-DOWN aerial masterplan of a new neighborhood.

Constraints:
- Output ONLY the final image prompt text (no markdown, no bullets explaining what you did).
- Make it specific: zoning, street hierarchy, block layout, parks, civic facilities.
- Avoid fantasy/sci-fi. This is a realistic planning rendering.

Project inputs:
- Families: {project_data.get('nombre_familles')}
- Avg family size: {project_data.get('taille_moyenne_famille')}
- Estimated population: {estimated_people}
- Land area: {land_hectares} hectares
- Budget level: {project_data.get('niveau_budget')}
- Planning priority: {project_data.get('priorite')}
- Housing type: {project_data.get('type_logement', 'mixed')}
- Allowed floors: {project_data.get('nombre_etages_autorises', 3)}
- Target green space: {project_data.get('pourcentage_espaces_verts', 25)}%

The image prompt MUST include:
- housing blocks (organized density), schools, health center(s), market area(s)
- a connected road network with sidewalks, intersections, and parking where appropriate
- parks/green corridors and public squares
- clean color palette, realistic textures, high clarity, professional urban planning diagram/render style
- scale/readability: clear separation of blocks and amenities
""".strip()

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=_get_text_model(),
        contents=instruction,
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text