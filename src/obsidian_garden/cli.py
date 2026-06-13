"""Command line interface for obsidian-garden."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .builder import build


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="obsidian-garden",
        description="Turn an Obsidian vault into a static digital garden site.",
    )
    parser.add_argument("vault", help="path to your Obsidian vault")
    parser.add_argument("-o", "--output", default="garden", help="output directory (default: ./garden)")
    parser.add_argument("-n", "--name", default="My Garden", help="site name shown in the header")
    parser.add_argument(
        "--publish-only",
        action="store_true",
        help="only build notes with 'publish: true' in frontmatter",
    )
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    try:
        count = build(Path(args.vault), Path(args.output), args.name, args.publish_only)
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"✓ built {count} pages -> {args.output}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
