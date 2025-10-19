#!/usr/bin/env python3

"""Compatibility wrapper for the new MiniDisplay CLI."""

from minidisplay.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
