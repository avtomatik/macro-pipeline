# 📦 ETL Flat Dataset

A lightweight, modular ETL pipeline built in Python using **Polars**, designed for reproducible data processing and containerized execution.

The project ingests raw macroeconomic datasets, applies transformations, and outputs a structured ZIP archive — all within a Dockerized environment.

---

## ⚙️ Features

* Modular ETL pipeline (load → transform → save)
* Built with **Polars** for fast columnar data processing
* Dockerized execution for reproducibility
* Clean separation of core pipeline components
* Produces compressed dataset outputs (`.zip`)

---

## 🧱 Project Structure

```
etl-flat-dataset/
├── etl_flat_dataset/
│   ├── core/
│   │   ├── paths.py
│   │   └── pipeline.py
│   └── main.py
├── data/
│   ├── raw/
│   └── processed/
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## 🚀 Running the Project

### 🐳 Using Docker (recommended)

#### Build image

```bash
docker build -t etl-flat-dataset .
```

#### Run pipeline (with persistent output)

```bash
docker run --rm \
  -v $(pwd)/data:/app/data \
  etl-flat-dataset
```

Output will be saved in:

```
data/processed/
```

---

## 🧪 Local Development (optional)

### Install dependencies

```bash
uv venv
source .venv/bin/activate

uv sync
```

### Run pipeline

```bash
uv run python -m etl_flat_dataset.main
```

---

## 📦 Output

The pipeline generates a compressed dataset:

```
data/processed/usa_macro_1950_2015.zip
```

---

## 🧠 Architecture Overview

The pipeline is composed of three main abstractions:

* **Loader** → reads raw CSV files
* **Transformer** → applies column transformations
* **Saver** → writes processed output (ZIP archive)

This design allows easy extension of the pipeline with new data sources or transformations.

---

## 🚧 Future Improvements

* Add CLI interface (`etl run`)
* Add config-driven pipeline definitions
* Parallel processing for large datasets
* Zig-based transformation module (experimental)
* S3 / cloud storage support

---

## 📜 License

MIT License
