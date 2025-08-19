from __future__ import annotations

import json
from typing import Optional

import click
from more_click import verbose_option

from .core import upload_cwd


@click.command()
@click.option("--title", required=True, help="Title for deposition")
@click.option("--description", required=True, help="Description / abstract")
@click.option("--creator", "creators", multiple=True, required=True, help="Repeatable: creator 'Family, Given'")
@click.option("--sandbox", is_flag=True, help="Use Zenodo sandbox (https://sandbox.zenodo.org)")
@click.option("--no-publish", is_flag=True, help="Create draft but do not publish")
@click.option("--dir", "directory", default=".", show_default=True, help="Directory to archive")
@click.option("--license", default="CC0-1.0", show_default=True, help="SPDX license identifier")
@click.option("--json", "json_out", is_flag=True, help="Print JSON response instead of URL")
@verbose_option  # type: ignore[misc]
@click.version_option()
def main(title: str, description: str, creators: list[str], sandbox: bool, no_publish: bool,
         directory: str, license: str, json_out: bool) -> None:
    """Zip directory and upload to Zenodo using existing credentials."""
    result = upload_cwd(title=title, description=description, creators=creators,
                        sandbox=sandbox, directory=directory, publish=not no_publish,
                        license=license)
    if json_out:
        print(json.dumps(result.response_json, indent=2))
    else:
        print(result.response_json["links"]["html"])


if __name__ == "__main__":  # pragma: no cover
    main()
