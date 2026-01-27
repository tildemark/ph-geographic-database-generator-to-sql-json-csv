# Open PH Geographic Data Platform (v2.2.0)

![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**A modern, containerized platform for Philippine Standard Geographic Code (PSGC) data.**

> **Note:** This project is a complete overhaul of the legacy v1.0 scraping scripts. If you are looking for the old PHP/Python crawlers, please switch to the `v1-legacy-crawler` branch.

## 🚀 Overview

The **Open PH Geographic Data Platform** provides a reliable, high-performance way to access Philippine geographic data (Regions, Provinces, Cities, Municipalities, Barangays).

Unlike the previous version which relied on fragile web scraping, v2.0.0+ uses a **verified ingestion workflow** where official PSGC Excel files are uploaded via a secure Admin Dashboard. This data is then served via:

1.  **Public API:** A high-speed, cached REST API (FastAPI + Redis) for real-time application usage.
2.  **Static Dumps:** Automatically generated `.sql`, `.json`, `.xml`, and `.csv` files for offline use.

**Live Demo:** [https://barangays.sanchez.ph](https://barangays.sanchez.ph)

## 🏗 Tech Stack

Built for performance and reliability on OCI Ampere (ARM64) infrastructure.

* **Database:** PostgreSQL 16 + PostGIS (Hierarchical integrity & geo-spatial readiness)
* **Backend:** Python FastAPI (Async, Auto-Documentation)
* **Caching:** Redis 7 (Rate limiting & response caching)
* **Frontend:** Next.js 14 (App Router), Tailwind CSS, Shadcn/UI
* **Infrastructure:** Docker Compose (Orchestration)

## ✨ Features

* **✅ Live Public API:** Query geographic data with sub-millisecond latency.
* **✅ Verified Data Ingest:** Admin interface to upload official PSGC Excel files, preventing "broken crawler" issues.
* **✅ Auto-Generation:** Instantly generates static SQL/JSON/CSV/XML dumps upon data update.
* **✅ Rate Limiting:** Built-in protection against abuse (via Redis).
* **✅ Interactive Docs:** Full Swagger UI (`/docs`) and Redoc (`/redoc`) support.
* **✅ Dockerized:** One-command deployment for any server.

## 🛠 Installation & Setup

### Prerequisites
* Docker & Docker Compose

### 1. Clone the Repository
```bash
git clone https://github.com/tildemark/ph-geographic-database-generator-to-sql-json-csv.git
cd ph-geographic-database-generator-to-sql-json-csv
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
# Database Credentials
POSTGRES_USER=admin
POSTGRES_PASSWORD=change_me_securely
POSTGRES_DB=ph_geo_db

# Security
ADMIN_SECRET=your_secret_upload_key

# Domain Configuration
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
ALLOWED_ORIGINS=https://yourdomain.com
```

### 3. Run with Docker

```bash
docker-compose up --build -d
```

* **Frontend:** Accessible at `http://localhost:3000`
* **API:** Accessible at `http://localhost:8000`
* **API Docs:** Accessible at `http://localhost:8000/docs`

## 🛠 Troubleshooting

### 1. "Invalid Password" Error during Startup
If the backend fails with `InvalidPasswordError`:
- **Stale Volumes**: If you changed the password in `.env` but the DB still reports an old password, Docker might be reusing a "zombie" volume. 
- **Resolution**: Reset the database volume (Note: This deletes data).
  ```bash
  docker compose down -v
  docker compose up -d
  ```

### 2. 502 Bad Gateway / Connection Failures
- **Network Collisions**: If your server runs multiple Docker stacks, a container named `db` or `redis` might resolve to the wrong stack. 
- **Resolution**: Use unique hostnames in `docker-compose.yml`. We have defaulted to `ph_geo_db` and `ph_geo_redis` to prevent this.

### 3. Missing Cities (e.g., Cebu City, CDO)
- Major cities (Highly Urbanized Cities) are often administratively independent from provinces.
- **Resolution**: Re-upload the PSGC Excel file via the `/admin` panel. The ingestion script has updated logic to map these cities to their geographic provinces for easier navigation.

### 4. Upload "Network Error" (via Nginx)
- Large Excel files might exceed the default Nginx upload limit.
- **Resolution**: Update your Nginx Proxy Manager / Nginx config:
  ```nginx
  client_max_body_size 50M;
  proxy_read_timeout 300s;
  ```

## 📖 API Usage

The API is free to use but rate-limited to ensure availability.

**Base URL:** `https://barangays.sanchez.ph/api`

### Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/regions` | List all regions |
| `GET` | `/regions/{code}/provinces` | Get all provinces in a region |
| `GET` | `/provinces/{code}/cities` | Get all cities/municipalities in a province |
| `GET` | `/cities/{code}/barangays` | Get all barangays in a city/municipality |

*For full parameter details, visit the [Swagger Documentation](https://barangays.sanchez.ph/api/docs).*

## 🔐 Admin Guide (Data Updates)

To update the dataset when PSA releases a new PSGC file:

1. Download the latest **PSGC Publication (Excel)** from the [PSA Website](https://psa.gov.ph/classification/psgc).
2. Navigate to `/admin` on your deployment.
3. Enter your `ADMIN_SECRET`.
4. Upload the `.xlsx` file.
5. **Wait:** The system will sync the database and regenerate all static download files.

## 🤝 Contributing

Contributions are welcome! Please ensure you use `docker-compose` for development to match the production environment.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

