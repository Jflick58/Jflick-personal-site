"""Typer CLI for local blog image generation."""

import sys
from pathlib import Path
from typing import Annotated

import typer

from .core import generate_image_local
from .models import ImageRequest

app = typer.Typer(help="Generate blog images matching the site's warm minimalist aesthetic.")


@app.command()
def generate(
    prompt: Annotated[str, typer.Argument(help=ImageRequest.model_fields["prompt"].description)],
    post_slug: Annotated[str | None, typer.Option(help=ImageRequest.model_fields["post_slug"].description)] = ImageRequest.model_fields["post_slug"].default,
    output: Annotated[str | None, typer.Option(help=ImageRequest.model_fields["output"].description)] = ImageRequest.model_fields["output"].default,
    index: Annotated[int, typer.Option(help=ImageRequest.model_fields["index"].description)] = ImageRequest.model_fields["index"].default,
    aspect_ratio: Annotated[str, typer.Option(help=ImageRequest.model_fields["aspect_ratio"].description)] = ImageRequest.model_fields["aspect_ratio"].default,
    model: Annotated[str, typer.Option(help=ImageRequest.model_fields["model"].description)] = ImageRequest.model_fields["model"].default,
    save_dir: Annotated[str, typer.Option(help=ImageRequest.model_fields["save_dir"].description)] = ImageRequest.model_fields["save_dir"].default,
) -> None:
    """Generate a blog image locally using gemimg."""
    req = ImageRequest(
        prompt=prompt,
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
        image_bytes = generate_image_local(
            req.prompt,
            aspect_ratio=req.aspect_ratio,
            model=req.model,
        )
    except RuntimeError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    out = dest / f"{req.filename}.webp"
    out.write_bytes(image_bytes)
    typer.echo(f"/{out}")
