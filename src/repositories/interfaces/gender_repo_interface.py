from .generic_repo_interface import GenericRepositoryInterface
from models import Gender


class GenderRepositoryInterface(GenericRepositoryInterface[Gender]):
    ...

