# Rust Backend for Tokenization Project

This directory contains a complete Rust implementation of the tokenization backend server using Warp.

## Features

- REST API for accessing tokenization components
- In-memory storage for fast access
- CSV parsing for initial data loading
- Static file serving for frontend files
- CORS support for cross-origin requests

## Prerequisites

To build and run the Rust backend, you need:

1. Rust and Cargo (https://www.rust-lang.org/)
2. Build tools for compiling native dependencies:
   - On Windows: Visual Studio Build Tools or MinGW-w64
   - On macOS: Xcode Command Line Tools
   - On Linux: build-essential package

## Building

To check if the code compiles without building dependencies:

```bash
cargo check
```

To build the release version:

```bash
cargo build --release
```

## Running

To run the server in development mode:

```bash
cargo run
```

To run the server in release mode:

```bash
cargo run --release
```

The server will start on http://127.0.0.1:3030

## API Endpoints

- `GET /api/components` - Get all components
- `GET /api/components/{main_type}` - Get components by main type
- `GET /api/components/{main_type}/{sub_type}` - Get components by main type and sub type

## Project Structure

- `src/main.rs` - Main server entry point
- `src/models.rs` - Data models and structures
- `src/routes.rs` - API route handlers
- `src/csv_parser.rs` - CSV parsing utilities
- `src/database.rs` - Database operations (in-memory implementation)

## Frontend Integration

The server serves the frontend files from the `../tokenize_frontend` directory:

- Static files are served from `/static/*`
- The root path `/` serves `index.html`
- All other paths also serve `index.html` to support SPA routing

## Testing

To run tests:

```bash
cargo test
```

## Troubleshooting

If you encounter compilation errors related to missing build tools:

1. Install Visual Studio Build Tools (Windows)
2. Install Xcode Command Line Tools (macOS)
3. Install build-essential package (Linux)

For Windows, you can run `setup_build_tools.bat` to get instructions for installing the required tools.