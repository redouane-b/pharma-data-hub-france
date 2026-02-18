"""Tests that the star schema DDL loads correctly into DuckDB."""

from pathlib import Path

import duckdb


SCHEMA_PATH = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"

EXPECTED_TABLES = [
    "dim_time",
    "dim_geography",
    "dim_hcp",
    "dim_molecule",
    "dim_establishment",
    "dim_lab",
    "fact_prescriptions",
    "fact_pharma_payments",
]


def _create_db_with_schema() -> duckdb.DuckDBPyConnection:
    """Create an in-memory DuckDB and execute the schema DDL."""
    conn = duckdb.connect(":memory:")
    ddl = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.execute(ddl)
    return conn


def test_schema_file_exists():
    assert SCHEMA_PATH.exists(), f"Schema file not found at {SCHEMA_PATH}"


def test_schema_loads_without_errors():
    conn = _create_db_with_schema()
    tables = conn.execute("SHOW TABLES").fetchall()
    table_names = [t[0] for t in tables]
    assert len(table_names) >= 8


def test_all_expected_tables_exist():
    conn = _create_db_with_schema()
    tables = conn.execute("SHOW TABLES").fetchall()
    table_names = [t[0] for t in tables]
    for expected in EXPECTED_TABLES:
        assert expected in table_names, f"Missing table: {expected}"


def test_schema_is_idempotent():
    """Running the DDL twice should not raise errors (CREATE IF NOT EXISTS)."""
    conn = duckdb.connect(":memory:")
    ddl = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.execute(ddl)
    conn.execute(ddl)  # Second run should not fail
    tables = conn.execute("SHOW TABLES").fetchall()
    assert len([t[0] for t in tables]) == 8


def test_dim_time_columns():
    conn = _create_db_with_schema()
    cols = conn.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_name = 'dim_time'"
    ).fetchall()
    col_names = {c[0] for c in cols}
    assert "time_key" in col_names
    assert "year" in col_names
    assert "month" in col_names
    assert "quarter" in col_names


def test_fact_prescriptions_columns():
    conn = _create_db_with_schema()
    cols = conn.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_name = 'fact_prescriptions'"
    ).fetchall()
    col_names = {c[0] for c in cols}
    assert "code_cip13" in col_names
    assert "nb_boites" in col_names
    assert "montant_rembourse" in col_names
    assert "annee" in col_names


def test_fact_pharma_payments_columns():
    conn = _create_db_with_schema()
    cols = conn.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_name = 'fact_pharma_payments'"
    ).fetchall()
    col_names = {c[0] for c in cols}
    assert "numero_rpps" in col_names
    assert "montant_ttc" in col_names
    assert "categorie" in col_names
    assert "lab_key" in col_names
