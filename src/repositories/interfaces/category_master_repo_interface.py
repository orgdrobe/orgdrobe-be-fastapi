from .generic_repo_interface import GenericRepositoryInterface
from models import CategoryMaster

class CategoryMasterRepositoryInterface(GenericRepositoryInterface[CategoryMaster]): 
    ...
