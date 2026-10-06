from dataclasses import dataclass
import io
from typing import Sequence

import filetype
from fastapi import UploadFile
from PIL import Image, ImageOps

from core.exceptions.image_exceptions import (
    CorruptedImage,
    ImageDecompressionBomb,
    ImageFileTooLarge,
    InvalidImageFormat,
)
from schemas.image import ValidatedImage
from services.interfaces.image_validator_service_interface import (
    ImageValidatorServiceInterface,
)


@dataclass
class ImageValidatorConfig:
    """Configuration parameters for image validation and normalization."""

    max_file_size_bytes: int = 5 * 1024 * 1024  # 5 MB
    max_dimension: int = 2560  # 2560 px
    max_image_pixels: int = 20_000_000  # 20 Mpx
    webp_quality: int = 85
    allowed_mime_types: tuple[str, ...] = (
        "image/webp",
        "image/jpeg",
        "image/png",
    )


class ImageValidatorService(ImageValidatorServiceInterface):
    def __init__(self, config: ImageValidatorConfig | None = None) -> None:
        self.config = config or ImageValidatorConfig()

        # Set safety limit on Pillow for decompression bomb prevention
        Image.MAX_IMAGE_PIXELS = self.config.max_image_pixels

    @property
    def max_file_size_bytes(self) -> int:
        return self.config.max_file_size_bytes

    @property
    def max_dimension(self) -> int:
        return self.config.max_dimension

    @property
    def max_image_pixels(self) -> int:
        return self.config.max_image_pixels

    @property
    def webp_quality(self) -> int:
        return self.config.webp_quality

    @property
    def allowed_mime_types(self) -> tuple[str, ...]:
        return self.config.allowed_mime_types

    async def validate_and_process(
        self,
        file: UploadFile,
        max_size_bytes: int | None = None,
        max_dimension: int | None = None,
    ) -> ValidatedImage:
        effective_max_size = max_size_bytes or self.max_file_size_bytes

        if file.size is not None and file.size > effective_max_size:
            raise ImageFileTooLarge(
                max_size_bytes=effective_max_size,
                actual_size_bytes=file.size,
            )

        content = await file.read()
        await file.seek(0)

        return self.validate_and_process_bytes(
            content=content,
            filename=file.filename,
            max_size_bytes=effective_max_size,
            max_dimension=max_dimension,
        )

    def validate_and_process_bytes(
        self,
        content: bytes,
        filename: str | None = None,
        max_size_bytes: int | None = None,
        max_dimension: int | None = None,
    ) -> ValidatedImage:
        effective_max_size = max_size_bytes or self.max_file_size_bytes
        effective_max_dimension = max_dimension or self.max_dimension

        self._validate_payload_size(content, effective_max_size)

        self._validate_mime_type(content)

        self._verify_image_integrity(content)

        processed_bytes, width, height = self._transform_and_encode(
            content=content,
            max_dimension=effective_max_dimension,
        )

        return ValidatedImage(
            content=processed_bytes,
            content_type="image/webp",
            format="WEBP",
            width=width,
            height=height,
            size_bytes=len(processed_bytes),
            original_filename=filename,
        )

    def _validate_payload_size(self, content: bytes, max_size: int) -> None:
        actual_size = len(content)
        if actual_size == 0:
            raise CorruptedImage("Image file is empty")

        if actual_size > max_size:
            raise ImageFileTooLarge(
                max_size_bytes=max_size,
                actual_size_bytes=actual_size,
            )

    def _validate_mime_type(self, content: bytes) -> None:
        header = content[:1024]
        kind = filetype.guess(header)

        if kind is None or kind.mime not in self.allowed_mime_types:
            raise InvalidImageFormat(
                detected_mime=kind.mime if kind else None,
                allowed_mimes=self.allowed_mime_types,
            )

    def _verify_image_integrity(self, content: bytes) -> None:
        Image.MAX_IMAGE_PIXELS = self.max_image_pixels
        try:
            with Image.open(io.BytesIO(content)) as raw_img:
                raw_img.verify()
        except Image.DecompressionBombError:
            raise ImageDecompressionBomb(max_pixels=self.max_image_pixels)
        except Exception as exc:
            raise CorruptedImage(f"Malformed or corrupted image file: {str(exc)}") from exc

    def _transform_and_encode(
        self, content: bytes, max_dimension: int
    ) -> tuple[bytes, int, int]:
        try:
            with Image.open(io.BytesIO(content)) as raw_img:
                img = ImageOps.exif_transpose(raw_img) or raw_img.copy()

                img = self._normalize_color_mode(img)

                self._downscale_if_needed(img, max_dimension)

                output_bytes = self._encode_to_webp(img)
                width, height = img.size

                return output_bytes, width, height

        except Image.DecompressionBombError:
            raise ImageDecompressionBomb(max_pixels=self.max_image_pixels)
        except Exception as exc:
            raise CorruptedImage(f"Failed to process and normalize image: {str(exc)}") from exc

    @staticmethod
    def _normalize_color_mode(img: Image.Image) -> Image.Image:
        has_transparency = img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        )
        if has_transparency:
            return img.convert("RGBA")
        if img.mode != "RGB":
            return img.convert("RGB")
        return img

    @staticmethod
    def _downscale_if_needed(img: Image.Image, max_dimension: int) -> None:
        if img.width > max_dimension or img.height > max_dimension:
            img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

    def _encode_to_webp(self, img: Image.Image) -> bytes:
        output_buffer = io.BytesIO()
        img.save(
            output_buffer,
            format="WEBP",
            quality=self.webp_quality,
            method=4,
        )
        return output_buffer.getvalue()