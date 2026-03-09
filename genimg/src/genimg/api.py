"""FastAPI server for remote image generation."""

import os

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .core import generate_image
from .models import ImageRequest

app = FastAPI(title="genimg")
security = HTTPBearer()


def _verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> None:
    expected = os.environ.get("API_KEY", "")
    if not expected or credentials.credentials != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/generate")
def generate(
    req: ImageRequest,
    _: None = Depends(_verify_token),
) -> Response:
    """Generate a blog image and return raw WebP bytes."""
    try:
        image_bytes = generate_image(
            req.prompt,
            style_prompt=req.style_prompt,
            aspect_ratio=req.aspect_ratio,
            model=req.model,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return Response(content=image_bytes, media_type="image/webp")
