mod core;
 
use std::fs;
use std::path::Path;
 
use anyhow::Result;
use core::paths::*;
use core::pipeline::*;
 
fn main() -> Result<()> {
    let pipeline = DataPipeline {
        loaders: vec![CsvLoader],
        transformers: vec![InsertIndicatorAndSwapCols],
        saver: ZipCsvSaver,
    };
 
    let input_paths: Vec<_> = fs::read_dir(data_raw_dir())?
        .filter_map(|entry| {
            let path = entry.ok()?.path();
            if path.is_file() {
                Some(path)
            } else {
                None
            }
        })
        .collect();
 
    let input_refs: Vec<&Path> =
        input_paths.iter().map(|p| p.as_path()).collect();
 
    let output_path = data_out_dir().join(FILE_NAME);
 
    pipeline.run(&input_refs, &output_path)?;
 
    Ok(())
}
