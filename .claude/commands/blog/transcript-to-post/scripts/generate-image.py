#!/usr/bin/env python3
"""Thin wrapper that delegates to the genimg CLI.

Requires genimg to be installed: `uv pip install -e genimg/`
"""

import sys
from pathlib import Path

# Allow running from repo root without installing
GENIMG_SRC = Path(__file__).resolve().parents[5] / "genimg" / "src"
if GENIMG_SRC.is_dir():
    sys.path.insert(0, str(GENIMG_SRC))

from genimg.cli import app

if __name__ == "__main__":
    app()
