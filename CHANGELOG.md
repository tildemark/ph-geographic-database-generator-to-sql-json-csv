# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2026-01-27

### Added
- **Production URL Snippets**: The Documentation Guide now dynamically displays live API URLs based on environment configuration instead of hardcoded `localhost`.
- **HUC Geo-Grouping**: Major cities like Cebu City, Cagayan de Oro City, and Davao City are now correctly grouped under their geographic provinces in the dropdown interfaces.

### Fixed
- **HUC Data Visibility**: Fixed a logic error in `ingest.py` where Highly Urbanized Cities (independent cities) were missing from the provincial lists.
- **Data Integrity**: Refined `clean_code` logic to prevent Region 10+ data from being incorrectly assigned to Region 1 when Excel strips leading zeros.
- **Frontend Crash**: Resolved a fatal JavaScript error on the `/docs-guide` page caused by a double `/api` prefix and missing defensive checks on API responses.
- **Deployment Connectivity**: Resolved `InvalidPasswordError` by implementing automatic URL-encoding for database credentials.
- **Network Collisions**: Standardized on unique hostnames (`ph_geo_db`, `ph_geo_redis`) to prevent 502 errors caused by container name collisions in shared environments.
- **Health Check Path**: Moved the health endpoint to `/api/health` to align with Nginx proxy forwarding rules.

## [2.1.0] - 2026-01-27

### Added
- **XML Support:** Replaced HTML data dumps with XML format for better interoperability.
- **Complete Dataset:** New "All" category allowing download of the entire database in a single file (JSON, CSV, SQL, XML).
- **Search:** "Search by Code" functionality on the landing page to quickly find location details by 10-digit PSGC code.
- **Documentation:** Added `docs/guide/TECHNICAL_REFERENCE.md` detailing HUC mapping and ingestion logic.

### Fixed
- **Generation:** Resolved issue where aggregated static files (`all.*`) were not being generated.
- **Compatibility:** Fixed Python 3.11 syntax error related to f-string backslashes in SQL generation.

## [2.0.0] - 2026-01-26

### 🚀 Major Overhaul
Complete re-architecture of the project from a standalone CLI script to a containerized Full-Stack Web Platform.

### Added
- **API:** Live public API endpoints (FastAPI) for querying Regions, Provinces, Cities, and Barangays.
- **Database:** PostgreSQL implementation with PostGIS support for hierarchical data integrity.
- **Caching:** Redis integration for high-performance API response caching and rate limiting.
- **Frontend:** Next.js 14+ (App Router) Landing Page and Admin Dashboard.
- **Infrastructure:** `docker-compose` orchestration for Web, API, DB, and Redis services.
- **Documentation:** Interactive Swagger UI (`/docs`) and Redoc (`/redoc`) for API testing.
- **Exports:** Automatic generation of static SQL, JSON, and CSV dumps upon data update.

### Changed
- **Ingestion Strategy:** Switched from fragile HTML scraping/crawling to a reliable "Admin Upload" workflow using official PSGC Excel files.
- **Tech Stack:** Migrated from pure Python/PHP scripts to a Python (Backend) + Node.js (Frontend) hybrid stack.

### Removed
- Legacy PHP crawling scripts.
- `cron` based weekly scraping (replaced by manual verified upload).

## [1.0.0] - 2024-XX-XX
- Initial release of the Python/PHP scraping scripts.
- CLI generation of JSON/SQL/CSV files.