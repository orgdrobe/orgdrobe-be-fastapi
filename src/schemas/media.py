from pydantic import Field

from schemas.base_model import CamelCaseBaseModel


class UploadedMediaOut(CamelCaseBaseModel):
    file_key: str = Field(description="Storage object key")
    url: str = Field(description="Presigned URL for direct access")
    width: int = Field(description="Width in pixels")
    height: int = Field(description="Height in pixels")
    size_bytes: int = Field(description="File size in bytes")


class BatchDeleteImagesRequest(CamelCaseBaseModel):
    image_ids: list[int] = Field(min_length=1, description="List of image IDs to delete")

