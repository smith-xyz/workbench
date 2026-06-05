use axum::{Router, extract::Path, http::StatusCode, response::Json, routing::get};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use tokio::net::TcpListener;
use tower_http::cors::CorsLayer;
use tower_http::trace::TraceLayer;
use tracing::info;

#[derive(Serialize, Deserialize, Clone)]
struct Item {
    id: u32,
    name: String,
    description: String,
}

#[derive(Serialize)]
struct ApiResponse<T> {
    success: bool,
    data: Option<T>,
    message: String,
}

#[derive(Deserialize)]
struct CreateItemRequest {
    name: String,
    description: String,
}

// In-memory storage for demo purposes
type ItemStore = std::sync::Arc<tokio::sync::RwLock<HashMap<u32, Item>>>;

#[tokio::main]
async fn main() {
    // Initialize tracing
    tracing_subscriber::fmt::init();

    // Create in-memory store
    let store = ItemStore::default();

    // Build our application with routes
    let app = Router::new()
        .route("/", get(health_check))
        .route("/health", get(health_check))
        .route("/items", get(get_items).post(create_item))
        .route("/items/{id}", get(get_item))
        .layer(TraceLayer::new_for_http())
        .layer(CorsLayer::permissive())
        .with_state(store);

    let listener = TcpListener::bind("0.0.0.0:3000").await.unwrap();

    info!("Server running on http://0.0.0.0:3000");
    info!("Available endpoints:");
    info!("  GET  /         - Health check");
    info!("  GET  /health   - Health check");
    info!("  GET  /items    - Get all items");
    info!("  POST /items    - Create new item");
    info!("  GET  /items/{{id}} - Get item by ID");

    axum::serve(listener, app).await.unwrap();
}

async fn health_check() -> Json<ApiResponse<String>> {
    Json(ApiResponse {
        success: true,
        data: Some("Web service is running".to_string()),
        message: "OK".to_string(),
    })
}

async fn get_items(
    axum::extract::State(store): axum::extract::State<ItemStore>,
) -> Json<ApiResponse<Vec<Item>>> {
    let items = store.read().await;
    let items_vec: Vec<Item> = items.values().cloned().collect();

    Json(ApiResponse {
        success: true,
        data: Some(items_vec),
        message: "Items retrieved successfully".to_string(),
    })
}

async fn get_item(
    Path(id): Path<u32>,
    axum::extract::State(store): axum::extract::State<ItemStore>,
) -> Result<Json<ApiResponse<Item>>, StatusCode> {
    let items = store.read().await;

    if let Some(item) = items.get(&id) {
        Ok(Json(ApiResponse {
            success: true,
            data: Some(item.clone()),
            message: "Item found".to_string(),
        }))
    } else {
        Err(StatusCode::NOT_FOUND)
    }
}

async fn create_item(
    axum::extract::State(store): axum::extract::State<ItemStore>,
    Json(payload): Json<CreateItemRequest>,
) -> Result<Json<ApiResponse<Item>>, StatusCode> {
    let mut items = store.write().await;

    let id = items.len() as u32 + 1;
    let item = Item {
        id,
        name: payload.name,
        description: payload.description,
    };

    items.insert(id, item.clone());

    Ok(Json(ApiResponse {
        success: true,
        data: Some(item),
        message: "Item created successfully".to_string(),
    }))
}
