use std::fs::File;
use std::io::Write;
use std::path::Path;
 
use anyhow::Result;
use polars::prelude::*;

use ::zip::write::FileOptions;
use ::zip::ZipWriter;
 

pub trait DataLoader {
    fn load(&self, path: &Path) -> Result<LazyFrame>;
}
 
pub trait DataTransformer {
    fn transform(&self, lf: LazyFrame) -> LazyFrame;
}
 
pub trait DataSaver {
    fn save(&self, df: &mut DataFrame, path: &Path) -> Result<()>;
}
 

pub struct CsvLoader;
 
impl DataLoader for CsvLoader {
    fn load(&self, path: &Path) -> Result<LazyFrame> {
        Ok(
            LazyCsvReader::new(path)
                .with_has_header(true)
                .finish()?
        )
    }
}
 

pub struct InsertIndicatorAndSwapCols;
 
impl DataTransformer for InsertIndicatorAndSwapCols {
    fn transform(&self, lf: LazyFrame) -> LazyFrame {
        // We need column names >> must inspect schema
        let schema = lf.schema().expect("schema available");
        let cols = schema.iter_names().collect::<Vec<_>>();
 
        if cols.len() < 2 {
            return lf;
        }
 
        let year_col = cols[0].to_string();
        let value_col = cols.last().unwrap().to_string();
 
        lf.select([
            col(&year_col).alias("year"),
            col(&value_col)
                .cast(DataType::Float64)
                .alias("value"),
            lit(value_col.clone()).alias("indicator"),
        ])
    }
}
 

pub struct ZipCsvSaver;
 
impl DataSaver for ZipCsvSaver {
    fn save(&self, df: &mut DataFrame, path: &Path) -> Result<()> {
        let zip_path = path.with_extension("zip");
 
        let file = File::create(zip_path)?;
        let mut zip = ZipWriter::new(file);
 
        let options = FileOptions::default();
 
        zip.start_file(
            path.file_name().unwrap().to_string_lossy(),
            options,
        )?;
 
        let mut buffer: Vec<u8> = Vec::new();

        CsvWriter::new(&mut buffer)
            .include_header(true)
            .finish(df)?;
 
        zip.write_all(&buffer)?;
        zip.finish()?;
 
        Ok(())
    }
}
 

pub struct DataPipeline<L, T, S>
where
    L: DataLoader,
    T: DataTransformer,
    S: DataSaver,
{
    pub loaders: Vec<L>,
    pub transformers: Vec<T>,
    pub saver: S,
}
 
impl<L, T, S> DataPipeline<L, T, S>
where
    L: DataLoader,
    T: DataTransformer,
    S: DataSaver,
{
    pub fn run(&self, input_paths: &[&Path], output_path: &Path) -> Result<()> {
        let mut plans: Vec<LazyFrame> = Vec::new();
 
        for path in input_paths {
            for loader in &self.loaders {
                let mut lf = loader.load(path)?;
 
                for transformer in &self.transformers {
                    lf = transformer.transform(lf);
                }
 
                plans.push(lf);
            }
        }
 
        // Combine all lazy frames
        let combined = concat(plans, UnionArgs::default())?;
 
        // Execute once
        let mut df = combined.collect()?;
 
        self.saver.save(&mut df, output_path)?;
 
        Ok(())
    }
}
