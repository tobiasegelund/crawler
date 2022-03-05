import os
import shutil
from pathlib import Path
from .exceptions import AlreadyInUse

__all__ = ["create_dir_if_not_exits", "define_filepath", "evaluate_destination_folder"]


def create_dir_if_not_exits(dir_name: str) -> None:
    directory = os.path.dirname(dir_name)
    if not os.path.exists(directory):
        os.makedirs(directory)


def remove_dir(dir_name: str) -> None:
    directory = os.path.dirname(dir_name)
    if os.path.exists(directory):
        shutil.rmtree(directory)
    else:
        raise ValueError("Directory doesn't exists")


def define_filepath(destination_folder: Path, name: str) -> Path:
    return destination_folder / name


def evaluate_destination_folder(destination_folder: Path) -> None:
    if destination_folder.exists():
        raise AlreadyInUse("Selected name of folder exists already")
    # if destination_folder.is_file():
    #     raise ValueError("Selected name of folder is occupied by a file")
