from .generic_repo_interface import GenericRepositoryInterface
from models import Usage


class UsageRepositoryInterface(GenericRepositoryInterface[Usage]):
    ...

