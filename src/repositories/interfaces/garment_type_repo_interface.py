from .generic_repo_interface import GenericRepositoryInterface
from models import GarmentType


class GarmentTypeRepositoryInterface(GenericRepositoryInterface[GarmentType]):
    ...

