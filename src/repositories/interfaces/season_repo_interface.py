from .generic_repo_interface import GenericRepositoryInterface
from models import Season


class SeasonRepositoryInterface(GenericRepositoryInterface[Season]):
    ...

