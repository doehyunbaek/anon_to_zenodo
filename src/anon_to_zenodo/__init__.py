"""anon_to_zenodo: simple utility to upload current directory as an anonymous Zenodo deposition.

This tiny helper relies on the existing zenodo_client.Zenodo class. It prepares a zip
archive of the current working directory (excluding a few common ignore patterns),
then creates (and publishes) a new deposition with minimal metadata supplied by the
caller.

Typical usage from Python:

>>> from anon_to_zenodo import upload_cwd
>>> record = upload_cwd(title="My Backup", description="Snapshot of project")
>>> print(record.json()["links"]["html"])  # Human-facing landing page

Command line usage (after `pip install -e .`):

$ python -m anon_to_zenodo --title "My Backup" --description "Snapshot" --creators "Doe, Jane" "Roe, Richard"

Note: The Zenodo access token must be configured via pystow as per zenodo_client.
"""
from __future__ import annotations

from .core import upload_cwd, zip_directory

__all__ = ["upload_cwd", "zip_directory"]
