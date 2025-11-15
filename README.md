# 🇵🇭 Philippine Standard Geographic Code (PSGC) Data Tools

**PSGC-to-SQL/CSV/JSON Generator & Exporter for Philippine Administrative Divisions (Python & PHP)**

This repository provides scripts to process the official **Philippine Standard Geographic Code (PSGC)** data and generate ready-to-use database assets for all administrative divisions (Regions, Provinces, Cities/Municipalities, and Barangays).

It supports generating **SQL INSERT statements** for database population and directly exporting the structured data to **CSV, JSON, and XML** formats.

## ✨ Key Features

* **Code Generators:** Scripts written in **Python** and **PHP** to parse the official PSGC Excel file.

* **Multi-Format Export:** Extracts and exports structured geographic data into **SQL, CSV, JSON, and XML** formats.

* **Database Schema:** Includes `create_tables.sql` to quickly set up your database structure.

* **Up-to-Date:** Designed to process the latest PSGC data released by the Philippine Statistics Authority (PSA).

## 🗺️ Understanding the PSGC Hierarchy

A clear understanding of the PSGC's 10-digit code structure is essential for database design and lookups. The codes define the nested administrative hierarchy:

| **Digits** | **Geographic Level** | **Example Code (for a Barangay)** | **Description** | 
 | ----- | ----- | ----- | ----- | 
| **1-2** | **Region** | **04** (CALABARZON) | The first two digits identify the region. | 
| **3-4** | **Province** | 04.**21** (Batangas) | Digits 3 and 4 identify the province (or HUC/ICC) within the region. | 
| **5-6** | **City/Municipality** | 0421.**04** (City of Batangas) | Digits 5 and 6 identify the city or municipality within the province. | 
| **7-10** | **Barangay** | 042104.**001** (Example Barangay Code) | Digits 7 through 10 identify the barangay. | 

## 🚀 Usage

### 1. Generating the SQL Database

This phase turns the raw PSGC Excel file into SQL data that can be imported into your database.

| **Script** | **Language** | **Function** | 
 | ----- | ----- | ----- | 
| `psgc_to_sql.py` | Python | **Generates the core SQL `INSERT` statements** for all geographic levels (regions, provinces, cities, municipalities, barangays) from the PSGC file. | 
| `psgc_to_sql.php` | PHP | **Generates the core SQL `INSERT` statements** as an alternative to the Python script. | 
| `xlsx_to_csv.py` | Python | Utility to convert the PSA's source PSGC Excel file (`.xlsx`) to a simpler CSV format. | 
| `create_tables.sql` | SQL | Contains the `CREATE TABLE` statements necessary to set up your database schema. | 

**Steps:**

1. **Get PSGC Data:** Download the latest PSGC Excel file (`.xlsx`) from the PSA website.

2. **Generate SQL:** Run either `psgc_to_sql.py` (Python) or `psgc_to_sql.php` (PHP).

3. **Setup Database:** Execute `create_tables.sql` to prepare your tables.

4. **Populate:** Import and execute the generated SQL `INSERT` statements.

### 2. Extracting Data from the Database

Once your database is populated, you can extract the data into other interchange formats.

| **Script** | **Language** | **Function** | 
 | ----- | ----- | ----- | 
| `extract_data.py` | Python | Connects to your running SQL database, queries the administrative division tables, and exports the results into **SQL, CSV, JSON, and XML** files. | 
| `extract_data.php` | PHP | Serves the same purpose as the Python script, using PHP to connect to and export data from your database. | 

**Steps:**

1. **Configure:** Update the database credentials (`db_config` in Python or `$dbConfig` in PHP) within the extraction script.

2. **Run:** Execute `extract_data.py` or `extract_data.php` to generate the exported files.

## 💾 Data Dumps & Releases

The PSGC data is updated periodically. To offer maximum utility, we provide **pre-extracted data dumps** in the **Releases** section of this repository.

* **Benefit:** Developers who only need the data can skip running the scripts and download the ready-to-use `.sql`, `.csv`, or `.json` files immediately.

* **Version Control:** Every release is tagged with the date of the source PSGC data (e.g., `v2025-Q1`) to clearly indicate its freshness.

## 🛠️ Future TO-DOs

We are working on these planned improvements to enhance the repository:

* **Static API Data Generation:** Update extraction scripts to generate highly optimized, organized **JSON files** (e.g., `regions.json`, `04-provinces.json`) for serving as a Static API via GitHub Pages or a CDN.
* **Automated Release Generation (GitHub Actions):** Implement an automated workflow to periodically run the data generation/extraction scripts, commit the new static JSON files, and automatically create a new GitHub Release with fresh data dumps.
* **SQLite Support:** Add scripts to generate a single, pre-populated SQLite database file for simple application integration.
* **Dynamic API Exploration (Future):** Explore creating a separate, truly dynamic API endpoint (using Flask/Python or similar) for complex querying and filtering, separate from the static files.
* **Documentation Hosting:** Generate and host API documentation using GitHub Pages (e.g., Jekyll or a custom HTML template).

## 📜 Requirements

* **Python:** Python 3.6 or higher (with `openpyxl` and `mysql.connector` libraries)

* **PHP:** PHP 7.0 or higher (with PDO extension enabled)

## 🤝 Contributing

Contributions are welcome! Feel free to open issues, suggest features, or submit pull requests.

## ⚖️ License

[MIT License](https://www.google.com/search?q=https://github.com/tildemark/psgc2sql/blob/main/LICENSE)
