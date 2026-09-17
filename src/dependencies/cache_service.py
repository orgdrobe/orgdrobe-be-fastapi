from services import CacheService
from services.interfaces import CacheServiceInterface

def get_cache_service() -> CacheServiceInterface:
    return CacheService()