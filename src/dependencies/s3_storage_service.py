from services import S3StorageService
from services.interfaces import S3StorageServiceInterface

_s3_storage_service = S3StorageService()

def get_s3_storage_service() -> S3StorageServiceInterface:
    """Provide singleton instance of S3StorageService."""
    return _s3_storage_service
