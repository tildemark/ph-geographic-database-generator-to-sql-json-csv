Act as a Senior Full-Stack Architect. I need to overhaul an existing legacy project into a modern, production-ready system called the "Open PH Geographic Data Platform." 

## Project Goal
Create a system that serves Philippine Standard Geographic Code (PSGC) data via a high-performance public API and provides static downloadable dumps (SQL, JSON, CSV). 

## The Tech Stack
- **Database:** PostgreSQL (with PostGIS extension enabled).
- **Caching & Rate Limiting:** Redis.
- **Backend:** Python FastAPI (Async).
- **Frontend:** Next.js 14+ (App Router), Tailwind CSS.
- **UI Library:** Shadcn/UI (Radix primitives).
- **Data Processing:** Pandas (for parsing Excel).
- **Infrastructure:** Docker Compose (orchestrating Web, API, DB, and Redis).

## Core Features & Requirements

### 1. The Database (PostgreSQL)
- Design a relational schema for `Regions`, `Provinces`, `Districts`, `Cities/Municipalities`, and `Barangays`.
- Ensure proper Foreign Key relationships (e.g., A Barangay belongs to a City).
- Include indices on commonly queried fields (codes, names).

### 2. The Backend (FastAPI)
- **Admin Ingest:** Create a secured endpoint `POST /admin/upload-psgc` that accepts the official PSGC Excel file.
  - Use `pandas` to parse the Excel file.
  - Clean and normalize the data.
  - Perform an "Upsert" operation to Postgres (update existing records, insert new ones).
  - **Auto-Generation:** Upon successful ingestion, trigger a background task that generates static `.json`, `.csv`, and `.sql` dump files and saves them to a public static folder.
  - **Cache Invalidation:** Flush Redis keys related to geographic data after update.
- **Public API:**
  - Create standard endpoints: `/api/regions`, `/api/regions/{code}/provinces`, etc.
  - **Documentation:** Ensure Swagger UI is available at `/docs`.
  - **Rate Limiting:** Implement `fastapi-limiter` with Redis to limit public usage (e.g., 60 req/min).
  - **Caching:** Cache generic GET responses in Redis for 24 hours.

### 3. The Frontend (Next.js + Shadcn/UI)
- **Landing Page (`/`):** - A clean, developer-focused landing page.
  - **Download Section:** Buttons to download the latest generated SQL, CSV, and JSON dumps.
  - **Live API Test:** A section showing the API Endpoint URL and a "Status" indicator (health check).
  - Links to "Full Documentation" and "Swagger API Docs".
- **Documentation Page (`/docs-guide`):** - A comprehensive guide on how to use the data and the API schema (separate from the Swagger UI).
- **Admin Dashboard (`/admin`):**
  - A password-protected (or simple env secret protected) route.
  - A File Upload UI (using Shadcn components) to drop the PSGC Excel file.
  - A progress indicator or status log showing the ingestion result.

## Deliverables
1. **Docker Compose:** A `docker-compose.yml` file that spins up the Next.js app, FastAPI service, Postgres, and Redis.
2. **Database Models:** SQLAlchemy or SQLModel definitions.
3. **API Logic:** The `main.py` and router files handling the upload and the read endpoints.
4. **Frontend Components:** The React code for the Landing Page and the Admin Upload form.

Please start by setting up the project structure and the `docker-compose.yml`.