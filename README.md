# 📦 Macro Pipeline (Rust)

A modular ETL pipeline written in **Rust** using **Polars**, designed to process macroeconomic datasets and produce a compressed output archive.

The project ingests raw CSV files, applies transformations, and writes a unified dataset to a ZIP file — all within a containerized environment.

---

## ⚙️ Features

* Modular ETL pipeline (load → transform → save)
* Built with **Polars (Rust)** for columnar data processing
* Lazy execution model with a single materialization step
* Dockerized for reproducible runs
* Outputs compressed datasets (`.zip`)

---

## 🧱 Project Structure

```
macro-pipeline/
├── src/
│   ├── core/
│   │   ├── mod.rs
│   │   ├── paths.rs
│   │   └── pipeline.rs
│   └── main.rs
├── data/
│   ├── raw/
│   └── processed/
├── Cargo.toml
├── Dockerfile
└── README.md
```

---

## 🚀 Running the Project

### 🐳 Using Docker

```bash
docker build -t macro-pipeline .

docker run --rm \
  -v $(pwd)/data:/app/data \
  macro-pipeline
```

Output will be written to:

```
data/processed/
```

---

## 🧪 Local Development

```bash
cargo run --release
```

---

## 📦 Output

```
data/processed/usa_macro_1950_2015.zip
```

---

## 🧠 Architecture Overview

The pipeline is composed of three abstractions:

* **Loader** → reads CSV files into Polars `LazyFrame`
* **Transformer** → applies schema normalization and transformations
* **Saver** → materializes the result and writes a ZIP archive

All datasets are combined into a single lazy execution plan and evaluated once.

---

## ⚠️ Notes

* The pipeline currently loads and processes all data in memory.
* Output is buffered before being written to the ZIP archive.
* This makes the implementation simple, but not optimized for large datasets.

---

## 🚧 Future Improvements

* Streaming / chunked processing to reduce memory usage
* CLI interface for configurable runs
* Schema validation and error handling improvements
* Support for alternative storage backends

---

## 📜 License

MIT License

---
