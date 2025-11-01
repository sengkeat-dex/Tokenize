use csv::ReaderBuilder;
use std::fs::File;
use crate::models::NewTokenizationComponent;

pub fn parse_csv(file_path: &str) -> Result<Vec<NewTokenizationComponent>, Box<dyn std::error::Error>> {
    let file = File::open(file_path)?;
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_reader(file);
    
    let mut components = Vec::new();
    
    for result in reader.records() {
        let record = result?;
        if record.len() >= 3 {
            let component = NewTokenizationComponent {
                main_type: record.get(0).unwrap_or("").to_string(),
                sub_type: record.get(1).unwrap_or("").to_string(),
                components: record.get(2).unwrap_or("").to_string(),
            };
            components.push(component);
        }
    }
    
    Ok(components)
}