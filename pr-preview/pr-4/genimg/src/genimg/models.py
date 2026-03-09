"""Shared Pydantic models used by both the CLI and API."""

from pydantic import BaseModel, Field


class ImageRequest(BaseModel):
    """Parameters for generating an image."""

    prompt: str = Field(description="Image subject description")
    style_prompt: str = Field(
        default="",
        description="Style instructions prepended to the prompt (e.g. aesthetic, palette, constraints)",
    )
    post_slug: str | None = Field(
        default=None,
        description="Post slug for auto-naming (e.g. 'the-intuition-gap')",
    )
    output: str | None = Field(
        default=None,
        description="Output filename without extension. Overrides post_slug naming.",
    )
    index: int = Field(default=1, description="Image index number for naming")
    aspect_ratio: str = Field(default="16:9", description="Aspect ratio")
    model: str = Field(
        default="gemini-2.0-flash-preview-image-generation",
        description="Gemini model to use",
    )
    save_dir: str = Field(
        default="assets/images/generated",
        description="Output directory for generated images",
    )

    @property
    def filename(self) -> str:
        if self.output:
            return self.output
        if self.post_slug:
            return f"{self.post_slug}-{self.index}"
        return f"generated-{self.index}"
