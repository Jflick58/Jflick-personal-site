#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["gemimg", "fire"]
# ///
"""Generate blog images matching the site's warm minimalist aesthetic."""

import os
import sys
from pathlib import Path

import fire
from gemimg import GemImg

STYLE_PREFIX = """## Style Requirements

- **Aesthetic**: Warm minimalist. Think: oak slats, white countertops, brass fixtures.
  Clean but not sterile. Handcrafted, not industrial.
- **Color palette**: Warm white (#f8f7f4) backgrounds, oak tones (#c49468),
  brass/gold accents (#b89048), near-black (#18171a) for contrast.
  NO cool blues, NO saturated primaries, NO neon.
- **Mood**: Contemplative, precise, quietly confident. Like a well-lit workspace
  at golden hour.
- **Composition**: Generous negative space. Off-center subjects. No clutter.
  The image should breathe.
- **Texture**: Subtle grain or warmth, like film photography or risograph.
  Not photorealistic, not cartoonish.

Aspects of the image composition that MUST be followed EXACTLY:
1. NO text, words, letters, numbers, or watermarks anywhere in the image
2. NO people or human figures
3. NO corporate/stock photo aesthetics
4. NO busy patterns or visual clutter
5. The image must work as a blog illustration at 740px wide

## Subject

"""


def _fix_proxy():
    """Strip googleapis.com from no_proxy so the egress proxy is used."""
    for var in ("no_proxy", "NO_PROXY"):
        if var in os.environ:
            os.environ[var] = ",".join(
                h for h in os.environ[var].split(",")
                if "googleapis.com" not in h and "google.com" not in h
            )


def generate(
    prompt: str,
    *,
    post_slug: str | None = None,
    output: str | None = None,
    index: int = 1,
    aspect_ratio: str = "16:9",
    model: str = "gemini-3-pro-image-preview",
    save_dir: str = "assets/images/generated",
):
    """Generate a blog image.

    Args:
        prompt: Image subject description.
        post_slug: Post slug for auto-naming (e.g. 'the-intuition-gap').
        output: Output filename without extension. Overrides post_slug naming.
        index: Image index number for naming.
        aspect_ratio: Aspect ratio (default 16:9).
        model: Gemini model to use.
        save_dir: Output directory.
    """
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set", file=sys.stderr)
        sys.exit(1)

    _fix_proxy()

    dest = Path(save_dir)
    dest.mkdir(parents=True, exist_ok=True)

    if output:
        filename = output
    elif post_slug:
        filename = f"{post_slug}-{index}"
    else:
        filename = f"generated-{index}"

    g = GemImg(model=model)
    try:
        gen = g.generate(STYLE_PREFIX + prompt, aspect_ratio=aspect_ratio, save=False)
    except Exception as e:
        print(f"Error: image generation failed — {e}", file=sys.stderr)
        sys.exit(1)

    out = dest / f"{filename}.webp"
    gen.image.save(str(out), format="WEBP", quality=85)
    print(f"/{out}")


if __name__ == "__main__":
    fire.Fire(generate)
