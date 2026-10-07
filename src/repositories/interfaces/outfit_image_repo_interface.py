from abc import abstractmethod
from .generic_repo_interface import GenericRepositoryInterface
from models import OutfitImage


class OutfitImageRepositoryInterface(GenericRepositoryInterface[OutfitImage]):
    @abstractmethod
    async def get_by_outfit_id(self, outfit_id: int) -> list[OutfitImage]: ...

