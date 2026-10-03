from services import ImageValidatorService
from services.interfaces import ImageValidatorServiceInterface


def get_image_validator_service() -> ImageValidatorServiceInterface:
    return ImageValidatorService()
