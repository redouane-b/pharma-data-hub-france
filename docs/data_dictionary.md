# PharmaScope France — Data Dictionary

## Join Key Reference

| Join Key | Format | Links |
|----------|--------|-------|
| `numero_rpps` | 11-digit string | dim_hcp ↔ fact_pharma_payments |
| `code_commune_insee` | 5-char string (e.g. `75056`) | dim_geography ↔ dim_hcp, dim_establishment |
| `code_cip13` | 13-digit string | dim_molecule ↔ fact_prescriptions |
| `code_atc` | Up to 7 chars (e.g. `A10BA02`) | ATC hierarchy in dim_molecule |
| `numero_finess_et` | 9-digit string | dim_establishment ↔ fact_pharma_payments |
| `code_departement` | 2-3 char string (e.g. `75`, `2A`) | Geographic aggregation level |

---

## Dimension Tables

### dim_time
Generated calendar table covering 2014-2026.

| Column | Type | Description |
|--------|------|-------------|
| time_key | INTEGER | Primary key. Format YYYYMM (e.g. 202401). YYYY00 for annual. |
| year | SMALLINT | Calendar year |
| month | SMALLINT | Month (1-12). NULL for annual rows. |
| quarter | SMALLINT | Quarter (1-4) |
| semester | SMALLINT | Semester (1-2) |
| month_name | VARCHAR | Month name (French) |
| quarter_label | VARCHAR | e.g. "2024-Q1" |
| year_label | VARCHAR | e.g. "2024" |

### dim_geography
Source: **INSEE COG** (Code Officiel Géographique)

| Column | Type | Source Field | Description |
|--------|------|-------------|-------------|
| geo_key | INTEGER | (surrogate) | Primary key |
| code_commune_insee | VARCHAR(5) | `COM` | INSEE commune code (natural key) |
| nom_commune | VARCHAR | `LIBELLE` | Commune name |
| type_commune | VARCHAR | `TYPECOM` | COM=commune, ARM=arrondissement municipal, COMA/COMD |
| code_departement | VARCHAR(3) | `DEP` | Department code |
| nom_departement | VARCHAR | (joined) | Department name |
| code_region | VARCHAR(2) | `REG` | Region code |
| nom_region | VARCHAR | (joined) | Region name |
| population | INTEGER | (enriched COG) | Municipal population |

### dim_hcp
Source: **RPPS / Annuaire Santé** (`ps-libreacces-personne-activite.txt`)

| Column | Type | Source Field | Description |
|--------|------|-------------|-------------|
| hcp_key | INTEGER | (surrogate) | Primary key |
| numero_rpps | VARCHAR(11) | `Numéro RPPS` | 11-digit national HCP identifier |
| nom_exercice | VARCHAR | `Nom d'exercice` | Practice name (may differ from civil name) |
| prenom_exercice | VARCHAR | `Prénom d'exercice` | Practice first name |
| code_profession | VARCHAR | `Code profession` | Profession code |
| libelle_profession | VARCHAR | `Libellé profession` | Médecin, Pharmacien, Infirmier, etc. |
| code_savoir_faire | VARCHAR | `Code savoir-faire` | Specialty/qualification code |
| libelle_savoir_faire | VARCHAR | `Libellé savoir-faire` | e.g. Endocrinologie-diabétologie |
| code_mode_exercice | VARCHAR | `Code mode exercice` | Exercise mode code |
| libelle_mode_exercice | VARCHAR | `Libellé mode exercice` | Libéral, Salarié, Bénévole |
| code_commune_exercice | VARCHAR(5) | `Code commune (coord. structure)` | FK → dim_geography |

### dim_molecule
Source: **BDPM** (multiple files: CIS_bdpm, CIS_CIP_bdpm, CIS_COMPO_bdpm, CIS_GENER_bdpm)

| Column | Type | Source File | Description |
|--------|------|------------|-------------|
| molecule_key | INTEGER | (surrogate) | Primary key |
| code_cip13 | VARCHAR(13) | CIS_CIP_bdpm | 13-digit presentation code (barcode) |
| code_cip7 | VARCHAR(7) | CIS_CIP_bdpm | Legacy 7-digit CIP code |
| code_cis | VARCHAR(8) | CIS_bdpm | BDPM speciality code |
| denomination_specialite | VARCHAR | CIS_bdpm | Drug trade name |
| forme_pharmaceutique | VARCHAR | CIS_bdpm | Pharmaceutical form |
| voie_administration | VARCHAR | CIS_bdpm | Route of administration |
| code_atc | VARCHAR(7) | Open Medic / external | ATC classification (Anatomical Therapeutic Chemical) |
| substance_active | VARCHAR | CIS_COMPO_bdpm | Active substance(s) |
| statut_amm | VARCHAR | CIS_bdpm | Marketing authorization status |
| is_generique | BOOLEAN | CIS_GENER_bdpm | Whether the drug is a generic |
| titulaire_amm | VARCHAR | CIS_bdpm | Marketing authorization holder (laboratory) |

### dim_establishment
Source: **FINESS**

| Column | Type | Source Field | Description |
|--------|------|-------------|-------------|
| establishment_key | INTEGER | (surrogate) | Primary key |
| numero_finess_et | VARCHAR(9) | `nofinesset` | Physical site FINESS number |
| numero_finess_ej | VARCHAR(9) | `nofinessej` | Parent legal entity FINESS number |
| raison_sociale | VARCHAR | `rs` | Establishment name |
| categorie_code | VARCHAR(4) | `categetab` | Category code |
| categorie_libelle | VARCHAR | `libcategetab` | Category label (CHU, clinique, pharmacie, EHPAD...) |
| code_commune_insee | VARCHAR(5) | `commune` | FK → dim_geography |
| latitude / longitude | DOUBLE | Geocoded version | GPS coordinates |

### dim_lab
Source: **Transparence Santé** + BDPM titulaire_amm

| Column | Type | Description |
|--------|------|-------------|
| lab_key | INTEGER | Primary key |
| lab_name_raw | VARCHAR | Raw company name from source |
| lab_name_clean | VARCHAR | Normalized name (future ETL: fuzzy dedup) |
| siren | VARCHAR(9) | SIREN number if available |

---

## Fact Tables

### fact_prescriptions
Source: **Open Medic** (annual CSVs 2014-2024)

Grain: one row per (year, prescriber dept, executor dept, profession, age group, sex, CIP13)

| Column | Type | Source Field | Description |
|--------|------|-------------|-------------|
| nb_boites | BIGINT | `boites` | Number of boxes dispensed |
| nb_remboursements | BIGINT | `nbc` | Number of reimbursements |
| montant_rembourse | DECIMAL | `REM` | Amount reimbursed in euros |
| base_remboursement | DECIMAL | `BSE` | Reimbursement base in euros |
| code_cip13 | VARCHAR(13) | `CIP13` | Drug presentation code → dim_molecule |
| age_group | VARCHAR | `AGE` | Patient age bracket |
| sex | SMALLINT | `sexe` | 1=Male, 2=Female, 9=Unknown |

**Known limitations:**
- Data is aggregated (no individual prescription-level records)
- Cannot link to individual HCPs (only prescriber specialty/department)
- Encoding is Latin-1 with semicolon delimiters

### fact_pharma_payments
Source: **Transparence Santé** (EurosForDocs cleaned CSV)

Grain: one row per individual payment/advantage declaration

| Column | Type | Source Field | Description |
|--------|------|-------------|-------------|
| montant_ttc | DECIMAL | `montant` | Payment amount including tax (€) |
| categorie | VARCHAR | `categorie` | Convention, Avantage, Rémunération |
| numero_rpps | VARCHAR(11) | `rpps` | Beneficiary RPPS → dim_hcp |
| beneficiary_type | VARCHAR | `benef_categorie` | Professional or establishment |
| date_avantage | DATE | `date_avantage` | Date of the advantage/payment |

---

## Known Data Quality Issues ("Zones d'ombre")

| Issue | Impact | Mitigation |
|-------|--------|------------|
| Open Medic is aggregated, not individual-level | Cannot build individual HCP prescription profiles | Use for territory-level analysis; use Transparence Santé for HCP-level |
| Transparence Santé has free-text company names | dim_lab deduplication needed | EurosForDocs version handles some cleaning; fuzzy matching in ETL |
| FINESS EJ vs ET distinction | One legal entity can have multiple physical sites | Model both; join on ET for location analysis |
| RPPS file has multiple rows per professional | One activity row per practice location/specialty | Deduplicate by choosing primary activity |
| ANSM data not bulk-downloadable | No pharmacovigilance data in Sprint 1 | Stub created; revisit in future sprint |
| ATC codes in Open Medic vs BDPM may not align perfectly | Join gaps between prescription and drug reference data | Validate coverage during ETL |
