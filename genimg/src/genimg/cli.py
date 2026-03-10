"""Typer CLI for local blog image generation."""

import asyncio
import sys
from pathlib import Path
from typing import Annotated

import typer

from .core import generate_image
from .models import ImageRequest

app = typer.Typer(help="Generate images via Gemini with optional style prompts.")


@app.command()
def generate(
    prompt: Annotated[str, typer.Argument(help=ImageRequest.model_fields["prompt"].description)],
    style_prompt: Annotated[str, typer.Option(help=ImageRequest.model_fields["style_prompt"].description)] = ImageRequest.model_fields["style_prompt"].default,
    style_prompt_file: Annotated[Path | None, typer.Option(help="Path to a file containing style instructions (alternative to --style-prompt)")] = None,
    post_slug: Annotated[str | None, typer.Option(help=ImageRequest.model_fields["post_slug"].description)] = ImageRequest.model_fields["post_slug"].default,
    output: Annotated[str | None, typer.Option(help=ImageRequest.model_fields["output"].description)] = ImageRequest.model_fields["output"].default,
    index: Annotated[int, typer.Option(help=ImageRequest.model_fields["index"].description)] = ImageRequest.model_fields["index"].default,
    aspect_ratio: Annotated[str, typer.Option(help=ImageRequest.model_fields["aspect_ratio"].description)] = ImageRequest.model_fields["aspect_ratio"].default,
    model: Annotated[str, typer.Option(help=ImageRequest.model_fields["model"].description)] = ImageRequest.model_fields["model"].default,
    save_dir: Annotated[str, typer.Option(help=ImageRequest.model_fields["save_dir"].description)] = ImageRequest.model_fields["save_dir"].default,
) -> None:
    """Generate an image via the Gemini API."""
    resolved_style = style_prompt
    if style_prompt_file and style_prompt_file.is_file():
        resolved_style = style_prompt_file.read_text()

    req = ImageRequest(
        prompt=prompt,
        style_prompt=resolved_style,
        post_slug=post_slug,
        output=output,
        index=index,
        aspect_ratio=aspect_ratio,
        model=model,
        save_dir=save_dir,
    )

    dest = Path(req.save_dir)
    dest.mkdir(parents=True, exist_ok=True)

    try:
        image_bytes, mime_type = asyncio.run(generate_image(
            req.prompt,
            style_prompt=req.style_prompt,
            aspect_ratio=req.aspect_ratio,
            model=req.model,
        ))
    except RuntimeError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    ext = mime_type.split("/")[-1]
    out = dest / f"{req.filename}.{ext}"
    out.write_bytes(image_bytes)
    typer.echo(f"/{out}")
