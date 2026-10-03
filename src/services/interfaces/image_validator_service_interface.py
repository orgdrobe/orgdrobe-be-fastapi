from abc import ABC, abstractmethod

from fastapi import UploadFile

from schemas.image import ValidatedImage


class ImageValidatorServiceInterface(ABC):
    """Interface for validating, verifying, and normalizing uploaded image files."""

    @abstractmethod
    async def validate_and_process(
        self,
        file: UploadFile,
        max_size_bytes: int | None = None,
        max_dimension: int | None = None,
    ) -> ValidatedImage:
        """Validate uploaded file, check size and format, normalize, and encode to WebP."""
        ...

    @abstractmethod
    def validate_and_process_bytes(
        self,
        content: bytes,
        filename: str | None = None,
        max_size_bytes: int | None = None,
        max_dimension: int | None = None,
    ) -> ValidatedImage:
        """Validate raw image bytes, check size and format, normalize, and encode to WebP."""
        ...
