from __future__ import annotations

import argparse
import json
from typing import Sequence

from importlib.metadata import PackageNotFoundError, version

try:  # Resolve installed package version if available
    __version__ = version("anon-to-zenodo")
except PackageNotFoundError:  # pragma: no cover - during development / editable
    __version__ = "0.1.0"

__all__ = ["build_parser", "main"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="anon-to-zenodo",
        description="Zip directory and upload to Zenodo using existing credentials.",
    )
    parser.add_argument("--title", required=True, help="Title for deposition")
    parser.add_argument("--description", required=True, help="Description / abstract")
    parser.add_argument(
        "--creator",
        dest="creators",
        action="append",
        required=True,
        help="Repeatable: creator 'Family, Given'",
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use Zenodo sandbox (https://sandbox.zenodo.org)",
    )
    parser.add_argument(
        "--no-publish",
        action="store_true",
        help="Create draft but do not publish",
    )
    parser.add_argument(
        "--dir",
        dest="directory",
        default=".",
        help="Directory to archive (default: %(default)s)",
    )
    parser.add_argument(
        "--license",
        default="CC0-1.0",
        help="SPDX license identifier (default: %(default)s)",
    )
    parser.add_argument(
        "--json",
        dest="json_out",
        action="store_true",
        help="Print JSON response instead of URL",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (repeat for more)",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Lazy import so --help / --version work without optional runtime deps installed yet
    try:
        if __package__:
            from .core import upload_cwd  # type: ignore
        else:  # pragma: no cover
            from core import upload_cwd  # type: ignore
    except Exception as e:  # pragma: no cover
        raise SystemExit(f"Failed to import core functionality: {e}")

    result = upload_cwd(
        title=args.title,
        description=args.description,
        creators=args.creators,
        sandbox=args.sandbox,
        directory=args.directory,
        publish=not args.no_publish,
        license=args.license,
    )
    if args.json_out:
        print(json.dumps(result.response_json, indent=2))
    else:
        print(result.response_json["links"]["html"])
    return 0


def main() -> None:  # pragma: no cover
    run()


if __name__ == "__main__":  # pragma: no cover
    main()
