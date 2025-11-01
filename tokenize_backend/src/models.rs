use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TokenizationComponent {
    pub id: u32,
    pub main_type: String,
    pub sub_type: String,
    pub components: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NewTokenizationComponent {
    pub main_type: String,
    pub sub_type: String,
    pub components: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApiResponse<T> {
    pub success: bool,
    pub data: Option<T>,
    pub message: Option<String>,
}

#[derive(Debug, Clone)]
pub struct InMemoryDatabase {
    pub components: Vec<TokenizationComponent>,
    pub main_type_index: HashMap<String, Vec<usize>>,
    pub sub_type_index: HashMap<(String, String), Vec<usize>>,
}