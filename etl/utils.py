"""Shared utilities for the ETL pipeline."""

from __future__ import annotations

import hashlib
import logging
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv


def setup_logging(name: str, level: int = logging.INFO) -> logging.Logger:
    """Configure a logger with timestamp and level formatting."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
        )
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def get_project_root() -> Path:
    """Return the project root directory (parent of etl/)."""
    return Path(__file__).resolve().parent.parent


def load_env() -> None:
    """Load .env file from project root."""
    env_path = get_project_root() / ".env"
    if env_path.exists():
        load_dotenv(env_path)


def get_config(key: str, default: str = "") -> str:
    """Get a configuration value from environment variables."""
    load_env()
    return os.getenv(key, default)


def get_raw_dir() -> Path:
    """Return the raw data directory, creating it if needed."""
    raw_dir = get_project_root() / get_config("DATA_RAW_DIR", "data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    return raw_dir


def sha256_file(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def make_http_client(timeout: float | None = None) -> httpx.AsyncClient:
    """Create a configured async HTTP client."""
    if timeout is None:
        timeout = float(get_config("DOWNLOAD_TIMEOUT_SECONDS", "600"))
    return httpx.AsyncClient(
        timeout=httpx.Timeout(timeout, connect=30.0),
        follow_redirects=True,
        headers={
            "User-Agent": "PharmaScope-France/0.1 (open-data-hub; +https://github.com)"
        },
    )


def sanitize_filename(name: str) -> str:
    """Clean a string for use as a filename."""
    return "".join(c if c.isalnum() or c in ".-_" else "_" for c in name)
