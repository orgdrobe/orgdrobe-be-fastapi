from abc import abstractmethod
from .generic_repo_interface import GenericRepositoryInterface
from models import Color


class ColorRepositoryInterface(GenericRepositoryInterface[Color]):
    @abstractmethod
    async def get_by_rgb(self, red: int, green: int, blue: int) -> Color | None: ...

