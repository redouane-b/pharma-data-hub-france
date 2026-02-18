"""Dataset registry — single source of truth for all data source metadata."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class DatasetConfig:
    """Configuration for a single open-data source."""

    name: str
    description: str
    source_type: str  # "datagouv_api" | "direct_url"
    encoding: str
    separator: str
    file_format: str  # "csv" | "txt" | "xlsx" | "zip"
    dataset_id: str | None = None  # data.gouv.fr dataset slug
    direct_urls: list[str] = field(default_factory=list)
    resource_filter: Callable[[dict], bool] | None = None
    notes: str = ""


# ---------------------------------------------------------------------------
# Resource filters — used to select the right files from data.gouv.fr API
# ---------------------------------------------------------------------------

def _rpps_filter(resource: dict) -> bool:
    """Keep only the main RPPS extraction TXT files."""
    title = (resource.get("title") or "").lower()
    url = (resource.get("url") or "").lower()
    return (
        url.endswith(".txt")
        and "libreacces" in (title + url)
        and "personne" in (title + url) or "savoirfaire" in (title + url) or "dipl" in (title + url)
    )


def _open_medic_filter(resource: dict) -> bool:
    """Keep Open Medic complete expenditure base CSVs."""
    title = (resource.get("title") or "").lower()
    url = (resource.get("url") or "").lower()
    return (
        ("open_medic" in title or "open_medic" in url)
        and ("csv" in (resource.get("format") or "").lower() or url.endswith(".csv"))
    )


def _finess_filter(resource: dict) -> bool:
    """Keep the main FINESS establishment CSV extractions."""
    title = (resource.get("title") or "").lower()
    url = (resource.get("url") or "").lower()
    fmt = (resource.get("format") or "").lower()
    return fmt == "csv" and ("etalab" in title or "stock" in title or "finess" in url)


def _insee_cog_filter(resource: dict) -> bool:
    """Keep commune, departement, and region CSV files from INSEE COG."""
    title = (resource.get("title") or "").lower()
    url = (resource.get("url") or "").lower()
    fmt = (resource.get("format") or "").lower()
    return fmt == "csv" and any(
        kw in (title + url)
        for kw in ["v_commune", "v_departement", "v_region", "v_pays"]
    )


# ---------------------------------------------------------------------------
# BDPM direct download URLs
# ---------------------------------------------------------------------------

BDPM_BASE_URL = "https://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier="
BDPM_FILES = [
    "CIS_bdpm.txt",
    "CIS_CIP_bdpm.txt",
    "CIS_COMPO_bdpm.txt",
    "CIS_HAS_SMR_bdpm.txt",
    "CIS_HAS_ASMR_bdpm.txt",
    "CIS_GENER_bdpm.txt",
    "CIS_CPD_bdpm.txt",
    "HAS_LiensPageCT_bdpm.txt",
]

# ---------------------------------------------------------------------------
# Dataset Registry
# ---------------------------------------------------------------------------

DATASETS: dict[str, DatasetConfig] = {
    "rpps": DatasetConfig(
        name="rpps",
        description="RPPS / Annuaire Santé — National HCP registry",
        source_type="datagouv_api",
        dataset_id="annuaire-sante-extractions-des-donnees-en-libre-acces-des-professionnels-intervenant-dans-le-systeme-de-sante-rpps",
        encoding="utf-8",
        separator="|",
        file_format="txt",
        resource_filter=_rpps_filter,
        notes="Main file ~800MB. Pipe-delimited.",
    ),
    "open_medic": DatasetConfig(
        name="open_medic",
        description="Open Medic — Prescription data (2014-2024)",
        source_type="datagouv_api",
        dataset_id="open-medic-base-complete-sur-les-depenses-de-medicaments-interregimes",
        encoding="latin-1",
        separator=";",
        file_format="csv",
        resource_filter=_open_medic_filter,
        notes="Latin-1 encoding, semicolon-delimited. One CSV per year.",
    ),
    "finess": DatasetConfig(
        name="finess",
        description="FINESS — Healthcare establishment registry",
        source_type="datagouv_api",
        dataset_id="finess-extraction-du-fichier-des-etablissements",
        encoding="utf-8",
        separator=";",
        file_format="csv",
        resource_filter=_finess_filter,
        notes="Includes geolocated and standard establishment files.",
    ),
    "insee_cog": DatasetConfig(
        name="insee_cog",
        description="INSEE COG — Official geographic code (communes, departments, regions)",
        source_type="datagouv_api",
        dataset_id="code-officiel-geographique-cog",
        encoding="utf-8",
        separator=",",
        file_format="csv",
        resource_filter=_insee_cog_filter,
        notes="Comma-separated UTF-8. Files hosted on insee.fr.",
    ),
    "transparence_sante": DatasetConfig(
        name="transparence_sante",
        description="Transparence Santé — Pharma-to-HCP payments (EurosForDocs cleaned)",
        source_type="direct_url",
        direct_urls=["https://www.eurosfordocs.fr/download/ts_declaration.csv"],
        encoding="utf-8",
        separator=",",
        file_format="csv",
        notes="EurosForDocs cleaned version. ~500MB+. Handles deduplication and RPPS matching.",
    ),
    "bdpm": DatasetConfig(
        name="bdpm",
        description="BDPM — Public drug database (specialties, compositions, presentations, SMR/ASMR)",
        source_type="direct_url",
        direct_urls=[f"{BDPM_BASE_URL}{f}" for f in BDPM_FILES],
        encoding="utf-8",
        separator="\t",
        file_format="txt",
        notes="Tab-separated. 8 small files (1-4MB each).",
    ),
    "ansm": DatasetConfig(
        name="ansm",
        description="data.ansm — Pharmacovigilance (stub: visualization platform, no bulk download)",
        source_type="direct_url",
        direct_urls=[],
        encoding="utf-8",
        separator=",",
        file_format="csv",
        notes="Visualization platform only. No bulk download available. Stub for future sprint.",
    ),
}
