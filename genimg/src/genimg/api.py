"""FastAPI server for remote image generation."""

import os

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .core import generate_image
from .models import ImageRequest

app = FastAPI(title="genimg")
security = HTTPBearer()


def _get_env(request: Request) -> dict:
    """Get environment — CF Worker env from scope, or os.environ fallback."""
    return getattr(request.scope.get("env"), "__dict__", None) or dict(os.environ)


async def _verify_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Request:
    env = _get_env(request)
    expected = env.get("API_KEY", "")
    if not expected or credentials.credentials != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return request


@app.post("/generate")
async def generate(
    req: ImageRequest,
    request: Request = Depends(_verify_token),
) -> Response:
    """Generate an image and return raw WebP bytes."""
    env = _get_env(request)
    gemini_key = env.get("GEMINI_API_KEY", "")

    try:
        image_bytes = await generate_image(
            req.prompt,
            style_prompt=req.style_prompt,
            aspect_ratio=req.aspect_ratio,
            model=req.model,
            gemini_api_key=gemini_key,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return Response(content=image_bytes, media_type="image/webp")
