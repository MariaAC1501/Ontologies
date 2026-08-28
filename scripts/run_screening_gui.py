#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# ///

"""Run the local browser interface for one blinded human screening sheet."""

from __future__ import annotations

import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from screening.gui_server import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
