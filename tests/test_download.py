"""Tests for the download pipeline configuration and utilities."""

from pathlib import Path

from etl.config import BDPM_FILES, DATASETS
from etl.download import _derive_filename, _should_skip
from etl.utils import get_project_root, sanitize_filename, sha256_file


def test_all_datasets_registered():
    expected = {"rpps", "open_medic", "finess", "insee_cog", "transparence_sante", "bdpm", "ansm"}
    assert set(DATASETS.keys()) == expected


def test_dataset_configs_have_required_fields():
    for name, cfg in DATASETS.items():
        assert cfg.name == name
        assert cfg.description
        assert cfg.source_type in ("datagouv_api", "direct_url")
        assert cfg.encoding in ("utf-8", "latin-1")


def test_datagouv_datasets_have_dataset_id():
    for name, cfg in DATASETS.items():
        if cfg.source_type == "datagouv_api":
            assert cfg.dataset_id, f"{name} is datagouv_api but has no dataset_id"
            assert cfg.resource_filter is not None, f"{name} needs a resource_filter"


def test_direct_url_datasets_have_urls():
    for name, cfg in DATASETS.items():
        if cfg.source_type == "direct_url" and name != "ansm":
            assert len(cfg.direct_urls) > 0, f"{name} has no direct_urls"


def test_bdpm_has_all_files():
    cfg = DATASETS["bdpm"]
    assert len(cfg.direct_urls) == len(BDPM_FILES)
    for url in cfg.direct_urls:
        assert "fichier=" in url


def test_open_medic_encoding():
    assert DATASETS["open_medic"].encoding == "latin-1"
    assert DATASETS["open_medic"].separator == ";"


def test_derive_filename_from_url():
    assert _derive_filename("https://example.com/data/file.csv") == "file.csv"


def test_derive_filename_from_bdpm_url():
    url = "https://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_bdpm.txt"
    assert _derive_filename(url) == "CIS_bdpm.txt"


def test_derive_filename_with_title_fallback():
    result = _derive_filename("https://example.com/download", title="My Dataset 2024")
    assert result.endswith(".dat")
    assert "My" in result


def test_should_skip_nonexistent_file(tmp_path):
    dest = tmp_path / "nonexistent.csv"
    assert _should_skip(dest, None) is False


def test_should_skip_existing_file_matching_size(tmp_path):
    dest = tmp_path / "test.csv"
    dest.write_text("hello")
    meta = {"size_bytes": dest.stat().st_size}
    assert _should_skip(dest, meta) is True


def test_should_skip_existing_file_different_size(tmp_path):
    dest = tmp_path / "test.csv"
    dest.write_text("hello")
    meta = {"size_bytes": 999999}
    assert _should_skip(dest, meta) is False


def test_sanitize_filename():
    assert sanitize_filename("hello world!.csv") == "hello_world_.csv"
    assert sanitize_filename("file-name_v2.txt") == "file-name_v2.txt"


def test_sha256_file(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hello")
    h = sha256_file(f)
    assert len(h) == 64
    assert h == sha256_file(f)  # Deterministic


def test_project_root():
    root = get_project_root()
    assert (root / "pyproject.toml").exists()
