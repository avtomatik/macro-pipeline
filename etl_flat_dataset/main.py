from etl_flat_dataset.core.paths import DATA_OUT_DIR, DATA_RAW_DIR, FILE_NAME
from etl_flat_dataset.core.pipeline import (CsvLoader, DataPipeline,
                                            InMemoryZipSaver,
                                            InsertIndicatorAndSwapCols)


def main() -> None:
    pipeline = DataPipeline(
        loaders=[CsvLoader()],
        transformers=[InsertIndicatorAndSwapCols()],
        saver=InMemoryZipSaver(),
    )

    input_paths = [
        p for p in DATA_RAW_DIR.iterdir() if not p.name.startswith(".")
    ]
    output_path = DATA_OUT_DIR / FILE_NAME

    pipeline.run(input_paths, output_path)


if __name__ == "__main__":
    main()
