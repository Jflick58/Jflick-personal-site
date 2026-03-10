"""Core image generation logic shared by CLI and API."""

import os

import httpx

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def _fix_proxy() -> None:
    """Strip googleapis.com from no_proxy so the egress proxy is used."""
    for var in ("no_proxy", "NO_PROXY"):
        if var in os.environ:
            os.environ[var] = ",".join(
                h
                for h in os.environ[var].split(",")
                if "googleapis.com" not in h and "google.com" not in h
            )


async def generate_image(
    prompt: str,
    *,
    style_prompt: str = "",
    aspect_ratio: str = "16:9",
    model: str = "gemini-3-pro-image-preview",
    gemini_api_key: str | None = None,
) -> tuple[bytes, str]:
    """Call the Gemini API and return (image_bytes, mime_type).

    Used by both the local CLI and the FastAPI server.
    """
    api_key = gemini_api_key or os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    _fix_proxy()

    full_prompt = style_prompt + prompt if style_prompt else prompt
    url = f"{GEMINI_BASE}/{model}:generateContent?key={api_key}"
    body = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"],
            "imageMimeType": "image/png",
        },
    }

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(url, json=body)
    if resp.status_code != 200:
        raise RuntimeError(f"Gemini API error ({resp.status_code}): {resp.text}")

    data = resp.json()
    for candidate in data.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            inline = part.get("inlineData", {})
            mime_type = inline.get("mimeType", "")
            if mime_type.startswith("image/"):
                import base64

                return base64.b64decode(inline["data"]), mime_type

    raise RuntimeError("No image returned by Gemini")
