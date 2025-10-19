"""Allow `python -m minidisplay` execution."""

from .cli import main


def run() -> int:
    return main()


if __name__ == "__main__":
    raise SystemExit(run())
