import io
import pytest
from PIL import Image
from fastapi.datastructures import UploadFile, Headers

from core.exceptions.image_exceptions import (
    CorruptedImage,
    ImageFileTooLarge,
    InvalidImageFormat,
)
from services.image_validator_service import ImageValidatorService


def _create_test_image(
    format: str = "PNG",
    size: tuple[int, int] = (100, 100),
    color: tuple[int, int, int] = (255, 0, 0),
) -> bytes:
    buffer = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buffer, format=format)
    return buffer.getvalue()


@pytest.fixture
def image_validator() -> ImageValidatorService:
    return ImageValidatorService(
        max_file_size_bytes=2 * 1024 * 1024,  # 2 MB for tests
        max_dimension=1000,
        max_image_pixels=5_000_000,
        webp_quality=80,
    )


def test_validate_and_process_png_success(image_validator: ImageValidatorService):
    png_bytes = _create_test_image(format="PNG", size=(200, 150))
    result = image_validator.validate_and_process_bytes(png_bytes, filename="test.png")

    assert result.content_type == "image/webp"
    assert result.format == "WEBP"
    assert result.width == 200
    assert result.height == 150
    assert result.size_bytes == len(result.content)
    assert result.original_filename == "test.png"

    # Verify that content is a valid WebP image readable by PIL
    with Image.open(io.BytesIO(result.content)) as out_img:
        assert out_img.format == "WEBP"


def test_validate_and_process_jpeg_success(image_validator: ImageValidatorService):
    jpeg_bytes = _create_test_image(format="JPEG", size=(300, 200))
    result = image_validator.validate_and_process_bytes(jpeg_bytes, filename="photo.jpg")

    assert result.content_type == "image/webp"
    assert result.format == "WEBP"
    assert result.width == 300
    assert result.height == 200


def test_file_size_limit_exceeded(image_validator: ImageValidatorService):
    png_bytes = _create_test_image(format="PNG", size=(500, 500))
    # Test with custom max_size_bytes smaller than the image size
    with pytest.raises(ImageFileTooLarge) as exc_info:
        image_validator.validate_and_process_bytes(
            png_bytes,
            max_size_bytes=len(png_bytes) - 1,
        )

    assert exc_info.value.status_code == 413


def test_invalid_mime_type_raises_exception(image_validator: ImageValidatorService):
    fake_text = b"This is plain text and definitely not an image."
    with pytest.raises(InvalidImageFormat) as exc_info:
        image_validator.validate_and_process_bytes(fake_text)

    assert exc_info.value.status_code == 415


def test_empty_content_raises_corrupted_image(image_validator: ImageValidatorService):
    with pytest.raises(CorruptedImage) as exc_info:
        image_validator.validate_and_process_bytes(b"")

    assert exc_info.value.status_code == 400


def test_downscaling_when_exceeding_max_dimension(image_validator: ImageValidatorService):
    # Create image with width 1500 (limit is 1000)
    large_image_bytes = _create_test_image(format="PNG", size=(1500, 750))
    result = image_validator.validate_and_process_bytes(
        large_image_bytes,
        max_dimension=1000,
    )

    assert result.width == 1000
    assert result.height == 500  # Aspect ratio preserved (2:1)


@pytest.mark.asyncio
async def test_validate_upload_file(image_validator: ImageValidatorService):
    png_bytes = _create_test_image(format="PNG", size=(120, 80))
    upload_file = UploadFile(
        file=io.BytesIO(png_bytes),
        size=len(png_bytes),
        filename="upload.png",
        headers=Headers({"content-type": "image/png"}),
    )

    result = await image_validator.validate_and_process(upload_file)

    assert result.content_type == "image/webp"
    assert result.width == 120
    assert result.height == 80
    assert result.original_filename == "upload.png"
