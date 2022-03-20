from pathlib import Path

__all__ = ["create_dir_if_not_exits", "define_file_name", "remove_dir_if_exists"]


def create_dir_if_not_exits(dir_name: Path, force: bool = False) -> None:
    dir_name.mkdir(parents=True, exist_ok=True)


def remove_dir_if_exists(dir_name: Path) -> None:
    if dir_name.exists():
        dir_name.rmdir()


def define_file_name(dir: Path, name: str) -> Path:
    return dir.joinpath(name)


def create_tree_structure(name: Path) -> None:
    raise NotImplementedError()
