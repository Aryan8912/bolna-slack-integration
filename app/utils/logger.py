"""
app/utils/logger.py

Centralised logging setup. Import `logger` everywhere.
"""

import logging
import sys
from app.core.config import settings


def _setup() -> logging.Logger:
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    log = logging.getLogger("bolna_slack")
    log.setLevel(level)
    log.addHandler(handler)
    log.propagate = False
    return log


logger = _setup()