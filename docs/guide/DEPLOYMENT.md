# Production Deployment Guide (OCI + Portainer)

This guide details the "Best Method" to deploy the Open PH Geographic Data Platform on an **Oracle Cloud Infrastructure (OCI) Always Free Ampere** instance using **Portainer** and **GitOps**.

## 🏗 Architecture Overview

We utilize a **GitOps** approach where Portainer pulls the configuration directly from GitHub. This ensures your production environment always matches the codebase.

```mermaid
graph TD
    User([User]) -->|HTTPS/443| LB[Reverse Proxy (Nginx Proxy Manager)]
    LB -->|/api/*| API[Backend Container :8000]
    LB -->|/*| Web[Frontend Container :3000]
    
    subgraph "OCI Ampere Instance"
        LB
        API
        Web
        DB[(PostGIS)]
        Redis[(Redis)]
    end
```

## 📋 Prerequisites

1.  **OCI Ampere Instance:** 4 OCPUs, 24GB RAM (Ubuntu 22.04 or Oracle Linux recommended).
2.  **Domain Name:** `barangays.sanchez.ph` pointing to your Instance Public IP.
3.  **Docker & Portainer:** Installed and running.
4.  **Reverse Proxy:** We strongly recommend **Nginx Proxy Manager (NPM)** running in a container, connected to a Docker network named `net`.

## 🚀 Deployment Steps

### 1. Prepare Docker Network
The stack communicates with the Reverse Proxy via an external network. Run this on your VPS terminal:

```bash
docker network create net
```

> **Note:** If you use a different proxy network name, update `docker-compose.yml` (Line 105) or override it in Portainer.

### 2. Deploy Stack via Portainer

1.  Login to **Portainer**.
2.  Go to **Stacks** > **Add stack**.
3.  Select **Repository**.
4.  **Name:** `ph-geo`
5.  **Repository URL:** `https://github.com/tildemark/ph-geographic-database-generator-to-sql-json-csv.git`
6.  **Branch:** `main` (or use a specific tag like `v2.1.0` for stability).
7.  **Environment variables:**
    Add the production values (do not use default text!).
    
    ```env
    POSTGRES_USER=admin_prod
    POSTGRES_PASSWORD=YOUR_STRONG_DB_PASSWORD
    POSTGRES_DB=ph_geo_db
    ADMIN_SECRET=YOUR_STRONG_UPLOAD_SECRET
    NEXT_PUBLIC_API_URL=https://barangays.sanchez.ph/api
    ALLOWED_ORIGINS=https://barangays.sanchez.ph
    ```
8.  Click **Deploy the stack**.

Portainer will clone the repo, build the Docker images natively on your ARM64 core (this is fast!), and start the services.

### 3. Configure Reverse Proxy (Nginx Proxy Manager)

You need two forwarding rules to handle the Frontend and Backend traffic locally.

#### Proxy Host 1: Main Application
-   **Domain Names:** `barangays.sanchez.ph`
-   **Scheme:** `http`
-   **Forward Hostname:** `ph_geo_web` (Container Name)
-   **Forward Port:** `3000`
-   **Block Common Exploits:** ✅
-   **SSL:** Request a new Let's Encrypt Certificate (Force SSL, HTTP/2).

#### Custom Locations (Crucial!)
In the **Custom Locations** tab of the *Same Proxy Host*:

**Location 1: API**
-   **Define location:** `/api`
-   **Scheme:** `http`
-   **Forward Hostname:** `ph_geo_api`
-   **Forward Port:** `8000`

**Location 2: Docs (Optional)**
-   **Define location:** `/docs`
-   **Scheme:** `http`
-   **Forward Hostname:** `ph_geo_api`
-   **Forward Port:** `8000`

**Location 3: Redoc (Optional)**
-   **Define location:** `/redoc`
-   **Scheme:** `http`
-   **Forward Hostname:** `ph_geo_api`
-   **Forward Port:** `8000`

**Location 4: OpenAPI JSON (Optional)**
-   **Define location:** `/openapi.json`
-   **Scheme:** `http`
-   **Forward Hostname:** `ph_geo_api`
-   **Forward Port:** `8000`

### 4. OCI Security List
Ensure your OCI VCN Security List allows Ingress traffic on:
-   **TCP 80** (HTTP)
-   **TCP 443** (HTTPS)
-   (Optional) **TCP 9443** (Portainer)
-   (Optional) **TCP 81** (NPM Admin)

Deny traffic on 3000/8000 from public internet for security.

## 🔄 Updating / Redeploying

When you push new code to GitHub:
1.  Go to Portainer > Stacks > `ph-geo`.
2.  Click **Pull and redeploy**.
3.  Toggle **"Re-pull image"** (even if building locally, this triggers a fresh pull/build).
4.  Click **Update**.

## 🛑 Troubleshooting

**Status: Offline?**
If the frontend says "System Status: Offline":
1.  Check the `/api/health` or `/regions` access directly via `https://barangays.sanchez.ph/api/regions`.
2.  If that gives 404/502, check Nginx Proxy Manager logs.
3.  Ensure the `net` network is attached to both Nginx and the Stack.

**Build Fails (ARM64)?**
The standard images (`python:3.11-slim`, `node:20-alpine`, `postgis/postgis`) support ARM64. If you see "exec format error", ensure you aren't forcing `platform: linux/amd64` in compose (we aren't).
