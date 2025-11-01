mod models;
mod csv_parser;
mod routes;

use tokio;
use warp::Filter;
use std::sync::{Arc, RwLock};
use models::{InMemoryDatabase, TokenizationComponent};
use csv_parser::parse_csv;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Starting Tokenization API server...");
    
    // Parse CSV data
    println!("Parsing CSV data...");
    let new_components = parse_csv("../tokenization_digital_wallet.csv")?;
    println!("Found {} components in CSV", new_components.len());
    
    // Create in-memory database
    let mut db = InMemoryDatabase {
        components: Vec::new(),
        main_type_index: std::collections::HashMap::new(),
        sub_type_index: std::collections::HashMap::new(),
    };
    
    // Insert components into database
    for (i, component) in new_components.iter().enumerate() {
        let id = i as u32 + 1;
        let token_component = TokenizationComponent {
            id,
            main_type: component.main_type.clone(),
            sub_type: component.sub_type.clone(),
            components: component.components.clone(),
        };
        
        // Add to components list
        db.components.push(token_component);
        
        // Update indexes
        let main_type = component.main_type.clone();
        db.main_type_index.entry(main_type).or_insert_with(Vec::new).push(i);
        
        let sub_type_key = (component.main_type.clone(), component.sub_type.clone());
        db.sub_type_index.entry(sub_type_key).or_insert_with(Vec::new).push(i);
        
        println!("Inserted component with ID: {}", id);
    }
    
    let db = Arc::new(RwLock::new(db));
    
    // Create API routes
    let cors = warp::cors()
        .allow_any_origin()
        .allow_methods(vec!["GET", "POST", "PUT", "DELETE"])
        .allow_headers(vec!["Content-Type"]);
    
    let api_routes = routes::components_routes(db.clone())
        .with(cors);
    
    // Serve static files (frontend)
    let static_files = warp::path("static")
        .and(warp::fs::dir("../tokenize_frontend"));
    
    // Serve index.html for the root path
    let index = warp::get()
        .and(warp::path::end())
        .and(warp::fs::file("../tokenize_frontend/index.html"));
    
    // Combine all routes
    let routes = api_routes
        .or(static_files)
        .or(index);
    
    println!("Server starting on http://127.0.0.1:3030");
    println!("Frontend available at http://127.0.0.1:3030/");
    println!("API endpoints available at http://127.0.0.1:3030/api/components");
    
    warp::serve(routes)
        .run(([127, 0, 0, 1], 3030))
        .await;
    
    Ok(())
}