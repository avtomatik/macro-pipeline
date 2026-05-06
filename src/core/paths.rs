use std::path::PathBuf;
 
pub fn data_raw_dir() -> PathBuf {
    PathBuf::from("data/raw")
}
 
pub fn data_out_dir() -> PathBuf {
    PathBuf::from("data/processed")
}
 
pub const FILE_NAME: &str = "usa_macro_1950_2015.csv";
