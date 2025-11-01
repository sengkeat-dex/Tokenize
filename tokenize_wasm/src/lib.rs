use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};
use wasm_bindgen::JsCast;
use web_sys::{Request, RequestInit, Response};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TokenizationComponent {
    pub id: u32,
    pub main_type: String,
    pub sub_type: String,
    pub components: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApiResponse {
    pub success: bool,
    pub data: Option<Vec<TokenizationComponent>>,
    pub message: Option<String>,
}

#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}

#[wasm_bindgen(start)]
pub fn main() {
    log("Tokenize WASM module loaded");
}

#[wasm_bindgen]
pub async fn fetch_components() -> JsValue {
    let mut opts = RequestInit::new();
    opts.method("GET");
    
    let request = Request::new_with_str_and_init(
        "http://localhost:3030/api/components",
        &opts,
    ).unwrap();
    
    let window = web_sys::window().unwrap();
    let resp_value = wasm_bindgen_futures::JsFuture::from(
        window.fetch_with_request(&request)
    ).await.unwrap();
    
    let resp: Response = resp_value.dyn_into().unwrap();
    let text = wasm_bindgen_futures::JsFuture::from(
        resp.text().unwrap()
    ).await.unwrap();
    
    let text_string = text.as_string().unwrap();
    log(&format!("Response: {}", text_string));
    
    // Parse the response
    match serde_json::from_str::<ApiResponse>(&text_string) {
        Ok(api_response) => {
            JsValue::from_serde(&api_response).unwrap()
        }
        Err(e) => {
            log(&format!("Error parsing response: {:?}", e));
            JsValue::NULL
        }
    }
}

#[wasm_bindgen]
pub fn greet(name: &str) -> String {
    format!("Hello, {}! Welcome to the Tokenization WASM module", name)
}

#[wasm_bindgen]
pub fn process_components(components: &JsValue) -> JsValue {
    match components.into_serde::<Vec<TokenizationComponent>>() {
        Ok(components_vec) => {
            log(&format!("Processing {} components", components_vec.len()));
            
            // Example processing: count components by main type
            let mut counts = std::collections::HashMap::new();
            for component in &components_vec {
                *counts.entry(component.main_type.clone()).or_insert(0) += 1;
            }
            
            // Convert to a serializable format
            let result: Vec<(String, usize)> = counts.into_iter().collect();
            JsValue::from_serde(&result).unwrap()
        }
        Err(e) => {
            log(&format!("Error processing components: {:?}", e));
            JsValue::NULL
        }
    }
}