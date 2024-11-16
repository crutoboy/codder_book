import shutil
import os
from functools import lru_cache
from uuid import uuid4

from .config import WORKSPACE


@lru_cache(256)
def get_path_to_workspace(id_workspace: str) -> str:
    if '/' in id_workspace:
        raise Exception('Secure error. Find stop symbol in id_program')
    path_to_workspace = os.path.join(WORKSPACE, id_workspace)
    return path_to_workspace


def create_workspace() -> str:
    """создаёт пространство и возвращает его id"""

    id_workspace = str(uuid4())
    path_to_workspace = get_path_to_workspace(id_workspace)
    os.makedirs(path_to_workspace)

    return id_workspace


def del_workspace(id_workspace):
    """удаляет пространство по id"""
    path_to_workspace = get_path_to_workspace(id_workspace)
    if not os.path.isdir(path_to_workspace):
        return None
    shutil.rmtree(path_to_workspace)