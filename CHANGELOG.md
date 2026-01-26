# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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