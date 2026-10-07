from abc import abstractmethod
from .generic_repo_interface import GenericRepositoryInterface
from models import GarmentImage


class GarmentImageRepositoryInterface(GenericRepositoryInterface[GarmentImage]):
    @abstractmethod
    async def get_by_garment_id(self, garment_id: int) -> list[GarmentImage]: ...

