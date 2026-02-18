-- ============================================================
-- PharmaScope France — DuckDB Star Schema
-- Sprint 1: Initial data model
--
-- 6 dimensions + 2 fact tables
-- Designed around pharma SFE use cases:
--   - Territory analysis (geography × prescriptions)
--   - HCP profiling (RPPS × engagement × prescriptions)
--   - Competitive intelligence (molecules × labs × payments)
-- ============================================================

-- ============================================================
-- DIMENSION: dim_time
-- Source: Generated calendar table (2014-2026)
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_time (
    time_key        INTEGER PRIMARY KEY,  -- YYYYMM format (e.g. 202401; YYYY00 for annual)
    year            SMALLINT NOT NULL,
    month           SMALLINT,             -- NULL for annual aggregates
    quarter         SMALLINT,
    semester        SMALLINT,
    month_name      VARCHAR(20),
    quarter_label   VARCHAR(10),          -- e.g. '2024-Q1'
    year_label      VARCHAR(4)
);

-- ============================================================
-- DIMENSION: dim_geography
-- Source: INSEE COG (v_commune, v_departement, v_region)
-- Natural key: code_commune_insee (5 chars)
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_geography (
    geo_key             INTEGER PRIMARY KEY,
    code_commune_insee  VARCHAR(5) NOT NULL UNIQUE,
    nom_commune         VARCHAR(200),
    type_commune        VARCHAR(10),          -- COM, ARM, COMA, COMD
    code_departement    VARCHAR(3),           -- '75', '2A', '971'
    nom_departement     VARCHAR(100),
    code_region         VARCHAR(2),
    nom_region          VARCHAR(100),
    population          INTEGER,
    UNIQUE (code_commune_insee)
);

-- ============================================================
-- DIMENSION: dim_hcp (Healthcare Professional)
-- Source: RPPS / Annuaire Santé
-- Natural key: numero_rpps (11-digit RPPS number)
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_hcp (
    hcp_key                     INTEGER PRIMARY KEY,
    numero_rpps                 VARCHAR(11) NOT NULL UNIQUE,
    nom_exercice                VARCHAR(100),
    prenom_exercice             VARCHAR(100),
    code_profession             VARCHAR(10),
    libelle_profession          VARCHAR(100),      -- Médecin, Pharmacien, etc.
    code_categorie_pro          VARCHAR(10),
    libelle_categorie_pro       VARCHAR(100),      -- Civil, Militaire
    code_savoir_faire           VARCHAR(10),
    libelle_savoir_faire        VARCHAR(200),      -- Specialty (Endocrinologie, etc.)
    code_mode_exercice          VARCHAR(5),
    libelle_mode_exercice       VARCHAR(100),      -- Libéral, Salarié, Bénévole
    code_commune_exercice       VARCHAR(5),        -- FK → dim_geography
    code_departement_exercice   VARCHAR(3)
);

-- ============================================================
-- DIMENSION: dim_molecule
-- Source: BDPM (CIS_bdpm, CIS_CIP_bdpm, CIS_COMPO_bdpm)
-- Natural key: code_cip13 (13-digit presentation code)
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_molecule (
    molecule_key            INTEGER PRIMARY KEY,
    code_cip13              VARCHAR(13) UNIQUE,
    code_cip7               VARCHAR(7),
    code_cis                VARCHAR(8),           -- BDPM speciality code
    denomination_specialite VARCHAR(500),          -- Drug trade name
    forme_pharmaceutique    VARCHAR(200),
    voie_administration     VARCHAR(200),
    code_atc                VARCHAR(7),           -- ATC classification
    libelle_atc             VARCHAR(500),
    substance_active        VARCHAR(500),
    dosage                  VARCHAR(200),
    statut_amm              VARCHAR(100),         -- AMM status
    type_procedure_amm      VARCHAR(100),
    is_generique            BOOLEAN,
    libelle_groupe_generique VARCHAR(500),
    titulaire_amm           VARCHAR(300)          -- Marketing authorization holder (lab)
);

-- ============================================================
-- DIMENSION: dim_establishment
-- Source: FINESS
-- Natural key: numero_finess_et (9-char FINESS number)
-- Note: EJ = legal entity, ET = physical site
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_establishment (
    establishment_key   INTEGER PRIMARY KEY,
    numero_finess_et    VARCHAR(9) NOT NULL UNIQUE,  -- Physical site FINESS
    numero_finess_ej    VARCHAR(9),                  -- Parent legal entity FINESS
    raison_sociale      VARCHAR(300),
    categorie_code      VARCHAR(4),
    categorie_libelle   VARCHAR(200),
    code_commune_insee  VARCHAR(5),                  -- FK → dim_geography
    code_departement    VARCHAR(3),
    adresse             VARCHAR(500),
    code_postal         VARCHAR(5),
    telephone           VARCHAR(20),
    date_ouverture      DATE,
    date_fermeture      DATE,
    latitude            DOUBLE,
    longitude           DOUBLE
);

-- ============================================================
-- DIMENSION: dim_lab (Pharmaceutical Laboratory)
-- Source: Transparence Santé + BDPM titulaire_amm
-- ============================================================
CREATE TABLE IF NOT EXISTS dim_lab (
    lab_key         INTEGER PRIMARY KEY,
    lab_name_raw    VARCHAR(300) NOT NULL UNIQUE,  -- Raw name from source
    lab_name_clean  VARCHAR(300),                  -- Normalized (future ETL)
    siren           VARCHAR(9),
    country         VARCHAR(100) DEFAULT 'France'
);

-- ============================================================
-- FACT: fact_prescriptions
-- Source: Open Medic (annual CSVs 2014-2024)
-- Grain: year × prescriber_dept × executor_dept × profession
--        × age_group × sex × CIP13
-- ============================================================
CREATE TABLE IF NOT EXISTS fact_prescriptions (
    prescription_key    BIGINT PRIMARY KEY,
    -- Dimension keys
    time_key            INTEGER NOT NULL,          -- FK → dim_time
    molecule_key        INTEGER,                   -- FK → dim_molecule (via CIP13)
    geo_prescriber_key  INTEGER,                   -- FK → dim_geography (prescriber dept)
    geo_executor_key    INTEGER,                   -- FK → dim_geography (executor/pharmacy dept)
    -- Degenerate dimensions (Open Medic grain)
    code_cip13          VARCHAR(13),
    hcp_profession_code VARCHAR(10),               -- Prescriber profession code
    age_group           VARCHAR(10),               -- Tranche d'âge
    sex                 SMALLINT,                  -- 1=M, 2=F, 9=Unknown
    annee               SMALLINT NOT NULL,
    -- Measures
    nb_boites           BIGINT,                    -- Boxes dispensed
    nb_remboursements   BIGINT,                    -- Reimbursement count
    montant_rembourse   DECIMAL(15,2),             -- Amount reimbursed (€)
    base_remboursement  DECIMAL(15,2),             -- Reimbursement base (€)
    -- Audit
    source_file         VARCHAR(100)
);

-- ============================================================
-- FACT: fact_pharma_payments
-- Source: Transparence Santé (EurosForDocs ts_declaration.csv)
-- Grain: one row per individual payment/advantage declaration
-- ============================================================
CREATE TABLE IF NOT EXISTS fact_pharma_payments (
    payment_key         BIGINT PRIMARY KEY,
    -- Dimension keys
    time_key            INTEGER,                   -- FK → dim_time
    hcp_key             INTEGER,                   -- FK → dim_hcp (via RPPS)
    establishment_key   INTEGER,                   -- FK → dim_establishment (via FINESS)
    lab_key             INTEGER,                   -- FK → dim_lab
    geo_key             INTEGER,                   -- FK → dim_geography
    -- Degenerate dimensions
    identifiant_unique  VARCHAR(50),
    numero_rpps         VARCHAR(11),
    numero_finess       VARCHAR(9),
    beneficiary_type    VARCHAR(50),               -- professionnel_sante | etablissement
    beneficiary_name    VARCHAR(300),
    -- Payment details
    categorie           VARCHAR(100),              -- Convention, Avantage, Rémunération
    sous_categorie      VARCHAR(200),
    nature_avantage     VARCHAR(200),
    objet               VARCHAR(500),
    -- Measures
    montant_ttc         DECIMAL(15,2),             -- Amount incl. tax (€)
    -- Dates
    date_signature      DATE,
    date_avantage       DATE,
    annee               SMALLINT,
    -- Audit
    source_file         VARCHAR(100)
);

-- ============================================================
-- INDEXES for common query patterns
-- ============================================================

-- Prescription queries
CREATE INDEX IF NOT EXISTS idx_rx_time ON fact_prescriptions(time_key);
CREATE INDEX IF NOT EXISTS idx_rx_molecule ON fact_prescriptions(molecule_key);
CREATE INDEX IF NOT EXISTS idx_rx_cip13 ON fact_prescriptions(code_cip13);
CREATE INDEX IF NOT EXISTS idx_rx_annee ON fact_prescriptions(annee);
CREATE INDEX IF NOT EXISTS idx_rx_geo_prescriber ON fact_prescriptions(geo_prescriber_key);

-- Payment queries
CREATE INDEX IF NOT EXISTS idx_pay_time ON fact_pharma_payments(time_key);
CREATE INDEX IF NOT EXISTS idx_pay_hcp ON fact_pharma_payments(hcp_key);
CREATE INDEX IF NOT EXISTS idx_pay_lab ON fact_pharma_payments(lab_key);
CREATE INDEX IF NOT EXISTS idx_pay_rpps ON fact_pharma_payments(numero_rpps);
CREATE INDEX IF NOT EXISTS idx_pay_annee ON fact_pharma_payments(annee);

-- Dimension lookups
CREATE INDEX IF NOT EXISTS idx_geo_commune ON dim_geography(code_commune_insee);
CREATE INDEX IF NOT EXISTS idx_geo_dept ON dim_geography(code_departement);
CREATE INDEX IF NOT EXISTS idx_hcp_rpps ON dim_hcp(numero_rpps);
CREATE INDEX IF NOT EXISTS idx_hcp_profession ON dim_hcp(code_profession);
CREATE INDEX IF NOT EXISTS idx_mol_cip13 ON dim_molecule(code_cip13);
CREATE INDEX IF NOT EXISTS idx_mol_atc ON dim_molecule(code_atc);
CREATE INDEX IF NOT EXISTS idx_est_finess ON dim_establishment(numero_finess_et);
