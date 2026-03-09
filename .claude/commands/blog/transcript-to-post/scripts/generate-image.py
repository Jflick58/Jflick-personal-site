#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["gemimg", "fire", "httpx"]
# ///
"""Generate blog images matching the site's warm minimalist aesthetic."""

import os
import sys
from pathlib import Path

import fire
import httpx

SCRIPT_DIR = Path(__file__).resolve().parent
STYLE_PROMPT = (SCRIPT_DIR / "image-style-prompt.md").read_text()


def _fix_proxy():
    """Strip googleapis.com from no_proxy so the egress proxy is used."""
    for var in ("no_proxy", "NO_PROXY"):
        if var in os.environ:
            os.environ[var] = ",".join(
                h for h in os.environ[var].split(",")
                if "googleapis.com" not in h and "google.com" not in h
            )


def _generate_remote(prompt: str, aspect_ratio: str) -> bytes:
    """Call the genimg Cloudflare Worker and return image bytes."""
    url = os.environ["IMAGE_GEN_URL"].rstrip("/") + "/generate"
    api_key = os.environ.get("IMAGE_GEN_API_KEY", "")

    resp = httpx.post(
        url,
        json={"prompt": prompt, "aspect_ratio": aspect_ratio},
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=120,
    )
    if resp.status_code != 200:
        try:
            detail = resp.json().get("error", resp.text)
        except Exception:
            detail = resp.text
        print(f"Error: remote generation failed ({resp.status_code}): {detail}", file=sys.stderr)
        sys.exit(1)

    return resp.content


def _generate_local(prompt: str, aspect_ratio: str, model: str) -> bytes:
    """Use gemimg locally and return WebP image bytes."""
    from io import BytesIO
    from gemimg import GemImg

    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set", file=sys.stderr)
        sys.exit(1)

    _fix_proxy()

    g = GemImg(model=model)
    gen = g.generate(STYLE_PROMPT + prompt, aspect_ratio=aspect_ratio, save=False)

    buf = BytesIO()
    gen.image.save(buf, format="WEBP", quality=85)
    return buf.getvalue()


def generate(
    prompt: str,
    *,
    post_slug: str | None = None,
    output: str | None = None,
    index: int = 1,
    aspect_ratio: str = "16:9",
    model: str = "gemini-2.0-flash-preview-image-generation",
    save_dir: str = "assets/images/generated",
):
    """Generate a blog image.

    Set IMAGE_GEN_URL (and IMAGE_GEN_API_KEY) to use the remote genimg
    worker. Otherwise falls back to local gemimg + GEMINI_API_KEY.

    Args:
        prompt: Image subject description.
        post_slug: Post slug for auto-naming (e.g. 'the-intuition-gap').
        output: Output filename without extension. Overrides post_slug naming.
        index: Image index number for naming.
        aspect_ratio: Aspect ratio (default 16:9).
        model: Gemini model to use (local mode only).
        save_dir: Output directory.
    """
    dest = Path(save_dir)
    dest.mkdir(parents=True, exist_ok=True)

    if output:
        filename = output
    elif post_slug:
        filename = f"{post_slug}-{index}"
    else:
        filename = f"generated-{index}"

    try:
        if os.environ.get("IMAGE_GEN_URL"):
            image_bytes = _generate_remote(prompt, aspect_ratio)
        else:
            image_bytes = _generate_local(prompt, aspect_ratio, model)
    except SystemExit:
        raise
    except Exception as e:
        print(f"Error: image generation failed — {e}", file=sys.stderr)
        sys.exit(1)

    out = dest / f"{filename}.webp"
    out.write_bytes(image_bytes)
    print(f"/{out}")


if __name__ == "__main__":
    fire.Fire(generate)
