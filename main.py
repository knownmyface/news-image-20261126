# news-image-20261126 — entrypoint
#
# The finished image (entry.png) already sits at the repo root,
# produced beforehand by render.py. This script only drops a copy
# of it where the harness looks for the deliverable:
# $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
# Python 3.13 standard library only; no network, no rendering.

from pathlib import Path
import os
import shutil


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    destination = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination / source.name)


if __name__ == "__main__":
    main()
