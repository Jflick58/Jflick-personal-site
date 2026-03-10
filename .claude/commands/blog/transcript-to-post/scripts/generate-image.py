#!/usr/bin/env python3
"""Generate a blog image via the Cloudflare Worker proxy.

Calls https://genimg.jflick-cors.workers.dev instead of Gemini directly,
since claude.ai blocks outbound Gemini API calls.

Usage mirrors the genimg CLI:
  generate-image.py "prompt text" [--style-prompt "..."] [--post-slug "..."]
                    [--output "filename"] [--index N] [--save-dir "path"]

Required env var: GENIMG_API_KEY
"""

import argparse
import os
import sys
import urllib.request
import json
from pathlib import Path

WORKER_URL = "https://genimg.jflick-cors.workers.dev/generate"


def main():
    parser = argparse.ArgumentParser(description="Generate a blog image via the genimg Worker")
    parser.add_argument("prompt", help="Image subject description")
    parser.add_argument("--style-prompt", default="", help="Style instructions prepended to the prompt")
    parser.add_argument("--style-prompt-file", default=None, help="Path to a file containing style instructions")
    parser.add_argument("--post-slug", default=None, help="Post slug for auto-naming (e.g. 'the-intuition-gap')")
    parser.add_argument("--output", default=None, help="Output filename without extension")
    parser.add_argument("--index", type=int, default=1, help="Image index number for naming")
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument("--model", default="gemini-3-pro-image-preview")
    parser.add_argument("--save-dir", default="assets/images/generated")
    args = parser.parse_args()

    api_key = os.environ.get("GENIMG_API_KEY", "")
    if not api_key:
        print("Error: GENIMG_API_KEY environment variable is not set", file=sys.stderr)
        sys.exit(1)

    style_prompt = args.style_prompt
    if args.style_prompt_file:
        p = Path(args.style_prompt_file)
        if p.is_file():
            style_prompt = p.read_text()

    payload = {
        "prompt": args.prompt,
        "style_prompt": style_prompt,
        "post_slug": args.post_slug,
        "output": args.output,
        "index": args.index,
        "aspect_ratio": args.aspect_ratio,
        "model": args.model,
        "save_dir": args.save_dir,
    }

    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        WORKER_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            content_type = resp.headers.get("Content-Type", "image/jpeg")
            image_bytes = resp.read()
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)

    # Derive extension from content-type
    ext = content_type.split("/")[-1].split(";")[0].strip()

    # Derive filename (mirrors ImageRequest.filename logic)
    if args.output:
        stem = args.output
    elif args.post_slug:
        stem = f"{args.post_slug}-{args.index}"
    else:
        stem = f"generated-{args.index}"

    dest = Path(args.save_dir)
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / f"{stem}.{ext}"
    out.write_bytes(image_bytes)
    print(f"/{out}")


if __name__ == "__main__":
    main()
