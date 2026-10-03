from pydantic import BaseModel, Field


class ValidatedImage(BaseModel):
    content: bytes = Field(description="Normalized image binary content (WebP encoded)")
    content_type: str = Field(default="image/webp", description="MIME type of the processed image")
    format: str = Field(default="WEBP", description="Image format")
    width: int = Field(description="Width in pixels")
    height: int = Field(description="Height in pixels")
    size_bytes: int = Field(description="Size in bytes")
    original_filename: str | None = Field(default=None, description="Original filename if available")
