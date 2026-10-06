from services import ImageValidatorService
from services.interfaces import ImageValidatorServiceInterface


_image_validator_service = ImageValidatorService()


def get_image_validator_service() -> ImageValidatorServiceInterface:
    """Provide singleton instance of ImageValidatorService."""
    return _image_validator_service
