"""Central logging configuration."""
from __future__ import annotations

import logging
import sys

from src.config import settings

_CONFIGURED = False


def setup_logging(level: str | None = None) -> None:
    """Configure the application's root logger.

    Parameters
    
    level : str, optional
        Log level to apply (e.g. "INFO", "DEBUG"). Defaults to
        ``settings.log_level`` when omitted.
    """
    global _CONFIGURED
    if _CONFIGURED:
        return

    resolved_level = (level or settings.log_level).upper()
    logging.basicConfig(
        level=resolved_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
    _CONFIGURED = True
