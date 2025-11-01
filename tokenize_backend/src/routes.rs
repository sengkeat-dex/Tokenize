use warp::Filter;
use crate::models::{ApiResponse, TokenizationComponent, InMemoryDatabase};
use std::sync::{Arc, RwLock};

pub fn components_routes(
    db: Arc<RwLock<InMemoryDatabase>>
) -> impl Filter<Extract = impl warp::Reply, Error = warp::Rejection> + Clone {
    let db_filter = warp::any().map(move || db.clone());
    
    // Get all components
    let get_all = warp::path!("api" / "components")
        .and(warp::get())
        .and(db_filter.clone())
        .and_then(get_all_components);
        
    // Get components by main type
    let get_by_type = warp::path!("api" / "components" / String)
        .and(warp::get())
        .and(db_filter.clone())
        .and_then(get_components_by_type);
        
    // Get components by main type and sub type
    let get_by_subtype = warp::path!("api" / "components" / String / String)
        .and(warp::get())
        .and(db_filter)
        .and_then(get_components_by_subtype);

    get_all.or(get_by_type).or(get_by_subtype)
}

async fn get_all_components(
    db: Arc<RwLock<InMemoryDatabase>>
) -> Result<impl warp::Reply, warp::Rejection> {
    let db_guard = db.read().unwrap();
    let response = ApiResponse {
        success: true,
        data: Some(db_guard.components.clone()),
        message: None,
    };
    Ok(warp::reply::json(&response))
}

async fn get_components_by_type(
    main_type: String,
    db: Arc<RwLock<InMemoryDatabase>>
) -> Result<impl warp::Reply, warp::Rejection> {
    let db_guard = db.read().unwrap();
    if let Some(indices) = db_guard.main_type_index.get(&main_type) {
        let components: Vec<TokenizationComponent> = indices
            .iter()
            .map(|&i| db_guard.components[i].clone())
            .collect();
        
        let response = ApiResponse {
            success: true,
            data: Some(components),
            message: None,
        };
        Ok(warp::reply::json(&response))
    } else {
        let response: ApiResponse<Vec<TokenizationComponent>> = ApiResponse {
            success: true,
            data: Some(vec![]),
            message: Some("No components found for this type".to_string()),
        };
        Ok(warp::reply::json(&response))
    }
}

async fn get_components_by_subtype(
    main_type: String,
    sub_type: String,
    db: Arc<RwLock<InMemoryDatabase>>
) -> Result<impl warp::Reply, warp::Rejection> {
    let db_guard = db.read().unwrap();
    let key = (main_type, sub_type);
    if let Some(indices) = db_guard.sub_type_index.get(&key) {
        let components: Vec<TokenizationComponent> = indices
            .iter()
            .map(|&i| db_guard.components[i].clone())
            .collect();
        
        let response = ApiResponse {
            success: true,
            data: Some(components),
            message: None,
        };
        Ok(warp::reply::json(&response))
    } else {
        let response: ApiResponse<Vec<TokenizationComponent>> = ApiResponse {
            success: true,
            data: Some(vec![]),
            message: Some("No components found for this type and subtype".to_string()),
        };
        Ok(warp::reply::json(&response))
    }
}