"""
Download pipeline for all PharmaScope France open-data sources.

Usage:
    python -m etl.download                       # Download all datasets
    python -m etl.download --datasets bdpm rpps   # Download specific datasets
    python -m etl.download --list                 # List available datasets
"""

from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm

from etl.config import BDPM_FILES, DATASETS, DatasetConfig
from etl.utils import (
    get_config,
    get_raw_dir,
    make_http_client,
    sanitize_filename,
    setup_logging,
    sha256_file,
)

logger = setup_logging("etl.download")


# ---------------------------------------------------------------------------
# Metadata tracking
# ---------------------------------------------------------------------------

def _load_metadata(dataset_dir: Path) -> dict:
    meta_path = dataset_dir / "_metadata.json"
    if meta_path.exists():
        return json.loads(meta_path.read_text(encoding="utf-8"))
    return {"dataset": dataset_dir.name, "files": {}}


def _save_metadata(dataset_dir: Path, metadata: dict) -> None:
    meta_path = dataset_dir / "_metadata.json"
    metadata["last_updated"] = datetime.now(timezone.utc).isoformat()
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------------------
# data.gouv.fr API resource discovery
# ---------------------------------------------------------------------------

async def discover_resources(
    client: httpx.AsyncClient,
    dataset_id: str,
    resource_filter: callable | None = None,
) -> list[dict]:
    """Fetch resource list from data.gouv.fr API and optionally filter."""
    api_base = get_config("DATAGOUV_API_BASE", "https://www.data.gouv.fr/api/1")
    url = f"{api_base}/datasets/{dataset_id}/"
    logger.info("Discovering resources for dataset: %s", dataset_id)

    resp = await client.get(url)
    resp.raise_for_status()
    data = resp.json()

    resources = data.get("resources", [])
    logger.info("Found %d total resources for %s", len(resources), dataset_id)

    if resource_filter:
        resources = [r for r in resources if resource_filter(r)]
        logger.info("After filtering: %d resources", len(resources))

    return resources


# ---------------------------------------------------------------------------
# Streaming file download
# ---------------------------------------------------------------------------

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=5, min=5, max=60))
async def stream_download(
    client: httpx.AsyncClient,
    url: str,
    dest: Path,
    desc: str | None = None,
) -> dict:
    """Stream-download a file with progress bar, retry on failure.

    Returns file metadata dict with size and hash.
    """
    part_file = dest.with_suffix(dest.suffix + ".part")
    dest.parent.mkdir(parents=True, exist_ok=True)

    async with client.stream("GET", url) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))

        with open(part_file, "wb") as f, tqdm(
            total=total or None,
            unit="B",
            unit_scale=True,
            desc=desc or dest.name,
            disable=total == 0,
        ) as pbar:
            async for chunk in response.aiter_bytes(chunk_size=65536):
                f.write(chunk)
                pbar.update(len(chunk))

    # Atomic rename
    part_file.rename(dest)

    file_hash = sha256_file(dest)
    file_size = dest.stat().st_size
    logger.info("Downloaded %s (%s bytes, sha256=%s...)", dest.name, file_size, file_hash[:12])

    return {
        "url": url,
        "size_bytes": file_size,
        "sha256": file_hash,
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Per-dataset download logic
# ---------------------------------------------------------------------------

async def download_dataset(config: DatasetConfig) -> dict:
    """Download all files for a single dataset. Returns metadata."""
    raw_dir = get_raw_dir()
    dataset_dir = raw_dir / config.name
    dataset_dir.mkdir(parents=True, exist_ok=True)

    metadata = _load_metadata(dataset_dir)
    downloaded_files = metadata.get("files", {})

    async with make_http_client() as client:
        if config.source_type == "datagouv_api" and config.dataset_id:
            resources = await discover_resources(
                client, config.dataset_id, config.resource_filter
            )
            for res in resources:
                url = res.get("url", "")
                title = res.get("title", "")
                # Derive filename from URL or title
                filename = _derive_filename(url, title)
                dest = dataset_dir / filename

                if _should_skip(dest, downloaded_files.get(filename)):
                    logger.info("Skipping %s (already downloaded)", filename)
                    continue

                logger.info("Downloading %s from %s", filename, url[:80])
                file_meta = await stream_download(client, url, dest, desc=filename)
                file_meta["source_title"] = title
                downloaded_files[filename] = file_meta

        elif config.source_type == "direct_url":
            for url in config.direct_urls:
                filename = _derive_filename(url)
                dest = dataset_dir / filename

                if _should_skip(dest, downloaded_files.get(filename)):
                    logger.info("Skipping %s (already downloaded)", filename)
                    continue

                logger.info("Downloading %s from %s", filename, url[:80])
                file_meta = await stream_download(client, url, dest, desc=filename)
                downloaded_files[filename] = file_meta

    metadata["files"] = downloaded_files
    metadata["encoding"] = config.encoding
    metadata["separator"] = config.separator
    metadata["notes"] = config.notes
    _save_metadata(dataset_dir, metadata)
    return metadata


def _derive_filename(url: str, title: str = "") -> str:
    """Extract a clean filename from a URL or resource title."""
    parsed = urlparse(url)

    # For BDPM URLs with query param ?fichier=
    if "fichier=" in url:
        for part in parsed.query.split("&"):
            if part.startswith("fichier="):
                return unquote(part.split("=", 1)[1])

    # Use the URL path basename
    basename = Path(unquote(parsed.path)).name
    if basename and "." in basename:
        return sanitize_filename(basename)

    # Fallback: use title
    if title:
        return sanitize_filename(title)[:80] + ".dat"

    return "unknown_file.dat"


def _should_skip(dest: Path, existing_meta: dict | None) -> bool:
    """Check if a file already exists and should be skipped."""
    if not dest.exists():
        return False
    if not existing_meta:
        return False
    # Skip if file exists and has same size as recorded
    return dest.stat().st_size == existing_meta.get("size_bytes", -1)


# ---------------------------------------------------------------------------
# ANSM stub
# ---------------------------------------------------------------------------

def _create_ansm_stub(raw_dir: Path) -> dict:
    """Create a README stub for the ANSM dataset (no bulk download available)."""
    ansm_dir = raw_dir / "ansm"
    ansm_dir.mkdir(parents=True, exist_ok=True)
    readme = ansm_dir / "README.md"
    readme.write_text(
        "# data.ansm — Pharmacovigilance Data\n\n"
        "This dataset is available at https://data.ansm.sante.fr/ as a visualization\n"
        "platform. There is no bulk CSV download.\n\n"
        "## Available data (via the platform)\n"
        "- Adverse effect declarations (BNPV)\n"
        "- Medication errors\n"
        "- Stock shortage reports (Trustmed)\n"
        "- Data available since 2014, updated annually (A-1)\n\n"
        "## Future work\n"
        "- Consider web scraping or API reverse-engineering in a future sprint\n"
        "- The underlying Open Medic and BDPM data are already covered by other downloads\n",
        encoding="utf-8",
    )
    logger.info("Created ANSM stub at %s", readme)
    return {
        "dataset": "ansm",
        "status": "stub",
        "notes": "Visualization platform only. No bulk download available.",
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

async def download_all(dataset_names: list[str] | None = None) -> dict[str, dict]:
    """Download all (or specified) datasets. Returns metadata per dataset."""
    results = {}
    raw_dir = get_raw_dir()

    targets = dataset_names or list(DATASETS.keys())

    for name in targets:
        if name not in DATASETS:
            logger.warning("Unknown dataset: %s (skipping)", name)
            continue

        config = DATASETS[name]
        logger.info("=" * 60)
        logger.info("Starting download: %s — %s", config.name, config.description)
        logger.info("=" * 60)

        if name == "ansm":
            results[name] = _create_ansm_stub(raw_dir)
            continue

        try:
            results[name] = await download_dataset(config)
            file_count = len(results[name].get("files", {}))
            logger.info("Completed %s: %d files downloaded", name, file_count)
        except Exception:
            logger.exception("Failed to download %s", name)
            results[name] = {"dataset": name, "status": "error"}

    return results


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Download PharmaScope France open datasets")
    parser.add_argument(
        "--datasets",
        nargs="+",
        choices=list(DATASETS.keys()),
        help="Specific datasets to download (default: all)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available datasets and exit",
    )
    args = parser.parse_args()

    if args.list:
        for name, cfg in DATASETS.items():
            print(f"  {name:25s} — {cfg.description}")
        return

    results = asyncio.run(download_all(args.datasets))

    print("\n" + "=" * 60)
    print("Download Summary")
    print("=" * 60)
    for name, meta in results.items():
        status = meta.get("status", "ok")
        file_count = len(meta.get("files", {}))
        if status == "stub":
            print(f"  {name:25s} — STUB (no bulk download)")
        elif status == "error":
            print(f"  {name:25s} — ERROR")
        else:
            print(f"  {name:25s} — {file_count} files")


if __name__ == "__main__":
    main()
