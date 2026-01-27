# Technical Reference & Implementation Guide

This guide documents the core logic, design decisions, and known constraints of the Open PH Geographic Data Platform.

## 1. Geographic Hierarchy & Mapping Logic

### The "Independent City" Challenge
The Philippine Standard Geographic Code (PSGC) classifies some cities as "Highly Urbanized Cities" (HUCs) or "Independent Component Cities" (ICCs). These cities are administratively independent of the province they are geographically located in.
- **PSGC Behavior:** In the official Excel file, these cities often have a parent code that doesn't map directly to a Province in the hierarchical sense used by most applications.
- **Our Solution:** We implement a **Geographic Mapping Layer** (`GEOGRAPHIC_PROVINCE_MAP`) in `ingest.py`. ensuring that cities like **Cebu City** are grouped under **Cebu Province** for easy dropdown navigation, even if they are administratively independent.

**Key Mappings:**
- **Metro Manila (NCR):** Treated as a "Region", with Districts acting as pseudo-provinces.
- **Zamboanga City:** Mapped to Zamboanga del Sur.
- **Davao City:** Mapped to Davao del Sur.
- **Angeles City:** Mapped to Pampanga.

### Barangay Parent Resolution
Some Barangays in the PSGC file refer to an intermediate organizational code (like a District) rather than the City directly.
- **Logic:** The ingestion script uses a **Longest Common Prefix** matching algorithm (`find_parent_city`) to correctly associate a Barangay with its parent Municipality/City based on the 10-digit code structure.

## 2. Data Ingestion Pipeline

The backend (`backend/app/ingest.py`) processes the uploaded Excel file in the following stages:
1.  **Parse:** Reads the 'PSGC' sheet using Pandas (ignoring headers to strictly rely on column indices).
2.  **Clean:** Pads all codes to 10 digits (`zfill(10)`).
3.  **Upsert:** Iterates through Levels (Reg -> Prov -> Dist -> City -> Bgy) and performs idempotent INSERT/UPDATE operations to PostgreSQL.
4.  **Flatten:** Uses Pandas to merge all levels into a single `master` DataFrame.
5.  **Export:** Generates static files (`.json`, `.csv`, `.sql`, `.xml`) in `frontend/public/downloads`.

## 3. Static File Generation

### Supported Formats
-   **JSON:** Standard nested array of objects.
-   **CSV:** Flattened hierarchy (Region, Province, City, Barangay columns). generated via Pandas Merge.
-   **SQL:** Consolidated `INSERT INTO` statements.
-   **XML:** Custom XML structure `<ph_geographic_data><regions>...</regions>...</ph_geographic_data>`.

### Implementation Nuance: XML Formatting
The XML generation uses manual string templating instead of an XML library to ensure maximum performance and simple dependency management. Special characters (`&`, `<`, `>`) are explicitly escaped.

> **Note on Python 3.11:** The container runs Python 3.11. Backslashes inside f-string expressions (e.g., `f"{val.replace('\', '')}"`) are **syntax errors** in this version. We use a helper function `_format_sql_value` to handle SQL escaping safely outside of f-strings.

## 4. Search Implementation
The frontend uses a client-side search approach for the "Search by Code" feature, but for the "Complete Dataset", relies on pre-generated static files. The backend API (`/api/search`) could be implemented in the future for server-side full-text search.

## 5. Deployment
reference `docker-compose.yml`.
-   **API:** Python FastApi (Uvicorn).
-   **Web:** Next.js (Node 20).
-   **DB:** PostgreSQL 16 (Alpine).
-   **Cache:** Redis 7.
