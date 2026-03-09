#!/usr/bin/env python3
"""Generate blog images matching the site's warm minimalist aesthetic.

Uses the gemimg library to generate images via Gemini's image model.
Expects GEMINI_API_KEY environment variable to be set.

Usage:
    python scripts/generate-image.py "A brass compass on warm white marble" \
        --post-slug the-intuition-gap --aspect-ratio 3:2 --index 1
"""

import argparse
import os
import sys
from pathlib import Path

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


def build_prompt(user_prompt: str) -> str:
    return STYLE_PREFIX + user_prompt


def main():
    parser = argparse.ArgumentParser(
        description="Generate blog images with the site's warm minimalist aesthetic."
    )
    parser.add_argument("prompt", help="Image subject description")
    parser.add_argument(
        "-o", "--output", help="Output filename (without extension)", default=None
    )
    parser.add_argument(
        "--post-slug",
        help="Post slug for auto-naming (e.g., 'the-intuition-gap')",
        default=None,
    )
    parser.add_argument(
        "--aspect-ratio",
        help="Aspect ratio (default: 16:9)",
        default="16:9",
    )
    parser.add_argument(
        "--save-dir",
        help="Output directory (default: assets/images/generated/)",
        default="assets/images/generated",
    )
    parser.add_argument(
        "--index",
        help="Image index number for naming (default: 1)",
        type=int,
        default=1,
    )

    args = parser.parse_args()

    if not os.environ.get("GEMINI_API_KEY"):
        print(
            "Error: GEMINI_API_KEY environment variable is not set",
            file=sys.stderr,
        )
        sys.exit(1)

    save_dir = Path(args.save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    # Determine output filename
    if args.output:
        filename = args.output
    elif args.post_slug:
        filename = f"{args.post_slug}-{args.index}"
    else:
        filename = f"generated-{args.index}"

    full_prompt = build_prompt(args.prompt)

    g = GemImg()
    try:
        gen = g.generate(
            full_prompt,
            aspect_ratio=args.aspect_ratio,
            save=False,
        )
    except Exception as e:
        print(f"Error: image generation failed — {e}", file=sys.stderr)
        print("Check that GEMINI_API_KEY is valid and the Gemini API is reachable.", file=sys.stderr)
        sys.exit(1)

    output_path = save_dir / f"{filename}.webp"
    gen.image.save(str(output_path), format="WEBP", quality=85)

    # Print relative path for easy Markdown embedding
    print(f"/{output_path}")


if __name__ == "__main__":
    main()
