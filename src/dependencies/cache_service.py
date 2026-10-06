from services import CacheService
from services.interfaces import CacheServiceInterface

def get_cache_service() -> CacheServiceInterface:
    """Provide CacheService instance."""
    return CacheService()