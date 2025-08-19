"""Core functionality for anon_to_zenodo.

We re-use the Zenodo client in this repository to create a deposition.
The process:
1. Build a zip archive of the current directory (optionally specify another path).
2. Prepare minimal metadata (title, description, creators) with sensible defaults.
3. Create and publish the deposition.

Anonymous uploads on Zenodo are only possible via the *sandbox* API unless the
access token is configured. Here we assume the user already configured a token via
PyStow (see zenodo_client docs). We set sandbox via argument.
"""
from __future__ import annotations

import io
import os
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from zenodo_client import Creator, Metadata, Zenodo

DEFAULT_IGNORE = {
    ".git",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    ".DS_Store",
    "build",
    "dist",
    "htmlcov",
}

ALWAYS_IGNORE_SUFFIXES = {".pyc", ".pyo"}


def _iter_paths(root: Path, ignore_names: set[str]) -> Iterable[Path]:
    for path in root.rglob("*"):
        name = path.name
        if any(part in ignore_names for part in path.parts):
            continue
        if path.is_file() and path.suffix in ALWAYS_IGNORE_SUFFIXES:
            continue
        if path.is_file():
            yield path


def zip_directory(directory: str | os.PathLike[str] = ".", *, output: str | None = None,
                  ignore: Sequence[str] | None = None) -> Path:
    """Create a zip archive of the given directory and return its path.

    If output is not given, creates `<directory name>.zip` in a temporary location (cwd).
    Ignores common cache / VCS dirs plus any provided in `ignore`.
    """
    root = Path(directory).resolve()
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    ignore_names = DEFAULT_IGNORE.union(ignore or [])
    archive_name = output or f"{root.name}.zip"
    archive_path = Path(archive_name).resolve()
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in _iter_paths(root, ignore_names):
            arcname = file_path.relative_to(root)
            zf.write(file_path, arcname.as_posix())
    return archive_path


@dataclass
class UploadResult:
    deposition_id: str
    response_json: dict
    archive_path: Path


def upload_cwd(*, title: str, description: str, creators: Sequence[str], sandbox: bool = False,
               directory: str | os.PathLike[str] = ".", publish: bool = True,
               license: str | None = "CC0-1.0") -> UploadResult:
    """Zip the target directory and upload to Zenodo.

    :param title: Title for the deposition.
    :param description: Long(er) description. Can include limited HTML (Zenodo permits basic tags).
    :param creators: Iterable of creator names in form "Family, Given".
    :param sandbox: Use Zenodo sandbox environment.
    :param directory: Directory to archive.
    :param publish: Whether to immediately publish (default True).
    :param license: SPDX identifier; default CC0-1.0.
    :returns: UploadResult with deposition id, response JSON and path to created archive.
    """
    archive = zip_directory(directory)
    md_creators = [Creator(name=name) for name in creators]
    metadata = Metadata(
        title=title,
        upload_type="dataset",
        description=description,
        creators=md_creators,
        license=license,
    )
    zen = Zenodo(sandbox=sandbox)
    res = zen.create(data=metadata, paths=[archive], publish=publish)
    return UploadResult(deposition_id=str(res.json()["id"]), response_json=res.json(), archive_path=archive)
