#[cfg(test)]
mod tests {
    use super::*;
    use warp::test::request;
    use std::sync::{Arc, RwLock};

    #[tokio::test]
    async fn test_get_all_components() {
        // Create a simple in-memory database for testing
        let db = Arc::new(RwLock::new(InMemoryDatabase {
            components: vec![],
            main_type_index: std::collections::HashMap::new(),
            sub_type_index: std::collections::HashMap::new(),
        }));
        
        let api = routes::components_routes(db);
        
        let resp = request()
            .method("GET")
            .path("/api/components")
            .reply(&api)
            .await;
            
        assert_eq!(resp.status(), 200);
    }
}