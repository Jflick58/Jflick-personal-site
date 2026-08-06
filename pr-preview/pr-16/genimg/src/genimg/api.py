"""FastAPI server for remote image generation."""

import os

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .core import generate_image
from .models import ImageRequest

app = FastAPI(title="genimg")
security = HTTPBearer()


class _Env:
    """Wraps CF Worker env (attribute access) or os.environ (dict access)."""

    def __init__(self, obj):
        self._obj = obj

    def get(self, key: str, default: str = "") -> str:
        if self._obj is not None:
            val = getattr(self._obj, key, None)
            return val if val is not None else default
        return os.environ.get(key, default)


def _get_env(request: Request) -> _Env:
    """Get environment — CF Worker env from scope, or os.environ fallback."""
    return _Env(request.scope.get("env"))


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
        image_bytes, mime_type = await generate_image(
            req.prompt,
            style_prompt=req.style_prompt,
            aspect_ratio=req.aspect_ratio,
            model=req.model,
            gemini_api_key=gemini_key,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return Response(content=image_bytes, media_type=mime_type)
