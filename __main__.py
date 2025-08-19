from __future__ import annotations

import argparse
import json
from pathlib import Path
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
    # Title default is resolved dynamically after parsing based on the directory name
    parser.add_argument(
        "--title",
        help="Title for deposition (default: directory name)",
    )
    # Description default fixed string per user requirement
    parser.add_argument(
        "--description",
        help="Description / abstract (default: 'automatic anonymization and uplaod to zenodo')",
    )
    parser.add_argument(
        "--creator",
        dest="creators",
        action="append",
        help="Repeatable: creator 'Family, Given' (default: 'Authors, Anonymous')",
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use Zenodo sandbox (https://sandbox.zenodo.org)",
    )
    parser.add_argument(
        "--publish",
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

    # Apply dynamic defaults if not provided
    if not args.title:
        # Derive from target directory (can be provided via --dir); fallback to cwd name
        target_dir = getattr(args, "directory", ".") or "."
        args.title = Path(target_dir).resolve().name
    if not args.description:
        args.description = "automatic anonymization and uplaod to zenodo"
    if not args.creators:
        args.creators = ["Authors, Anonymous"]

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
        publish=args.publish,
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
