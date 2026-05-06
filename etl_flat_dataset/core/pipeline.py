import io
import zipfile
from pathlib import Path
from typing import Protocol, Sequence

import polars as pl


class DataLoader(Protocol):
    def load(self, file_path: Path) -> pl.DataFrame: ...


class DataTransformer(Protocol):
    def transform(self, df: pl.DataFrame) -> pl.DataFrame: ...


class DataSaver(Protocol):
    def save(self, df: pl.DataFrame, file_path: Path) -> None: ...


class CsvLoader(DataLoader):
    def load(self, file_path: Path) -> pl.DataFrame:
        df = pl.read_csv(file_path)
        df = df.rename({df.columns[0]: "year"})
        return df


class InsertIndicatorAndSwapCols(DataTransformer):
    """
    Insert last column name as 'indicator', keep its values as 'value',
    while preserving 'year'.
    Final order: ['year', 'indicator', 'value'].
    """

    def transform(self, df: pl.DataFrame) -> pl.DataFrame:
        if df.width < 2:
            return df

        year_col = df.columns[0]
        value_col = df.columns[-1]

        return (
            df.select([year_col, value_col])
            .rename({year_col: "year", value_col: "value"})
            .with_columns(
                pl.col("value").cast(pl.Float64),
                pl.lit(value_col).alias("indicator"),
            )
            .select(["year", "indicator", "value"])
        )


class InMemoryZipSaver(DataSaver):
    """
    Saves a Polars DataFrame directly into a ZIP file in memory
    without creating intermediate CSV files on disk.
    """

    def save(self, df: pl.DataFrame, file_path: Path) -> None:
        csv_buffer = io.StringIO()
        df.write_csv(csv_buffer, include_header=True)
        csv_buffer.seek(0)

        with zipfile.ZipFile(
            file_path.with_suffix(".zip"),
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
        ) as archive:
            archive.writestr(file_path.name, csv_buffer.getvalue())


class DataPipeline:
    def __init__(
        self,
        loaders: Sequence[DataLoader],
        transformers: Sequence[DataTransformer],
        saver: DataSaver,
    ) -> None:
        self.loaders = loaders
        self.transformers = transformers
        self.saver = saver

    def run(self, input_paths: Sequence[Path], output_path: Path) -> None:
        frames: list[pl.DataFrame] = []

        for path in input_paths:
            for loader in self.loaders:
                chunk = loader.load(path)
                for transformer in self.transformers:
                    chunk = transformer.transform(chunk)
                frames.append(chunk)

        df = pl.concat(frames, how="vertical", rechunk=True)

        self.saver.save(df, output_path)
