# tokenize_wasm

This crate provides a WebAssembly module for interacting with the Tokenization API.

## Building

To build the WebAssembly module, you'll need to install `wasm-pack`:

```bash
cargo install wasm-pack
```

Then build the module:

```bash
wasm-pack build --target web
```

This will generate a `pkg` directory with the WASM module and JavaScript bindings.

## Usage

After building, you can use the module in your JavaScript application:

```javascript
import init, { fetch_components, greet, process_components } from './pkg/tokenize_wasm.js';

async function run() {
    // Initialize the WASM module
    await init();
    
    // Use the functions
    console.log(greet("World"));
    
    // Fetch components from the API
    const components = await fetch_components();
    console.log(components);
    
    // Process components
    const processed = process_components(components);
    console.log(processed);
}

run();
```

## Functions

- `greet(name: string) -> string`: Returns a greeting message
- `fetch_components() -> Promise<JsValue>`: Fetches components from the API
- `process_components(components: JsValue) -> JsValue`: Processes components and returns counts by type

## Prerequisites

- Rust and Cargo
- wasm-pack