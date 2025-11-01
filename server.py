#!/usr/bin/env python3
import http.server
import socketserver
import json
import csv
import urllib.parse
from http.server import BaseHTTPRequestHandler
import os
import sys

# Load components from CSV
def load_components():
    components = []
    with open('tokenization_digital_wallet.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            # Skip header row if it's somehow included
            if row['Main Type'] != 'Main Type':
                components.append({
                    'id': i + 1,
                    'main_type': row['Main Type'] or '',
                    'sub_type': row['Sub Type'] or '',
                    'components': row['Components'] or ''
                })
    return components

components = load_components()
print(f"Loaded {len(components)} components from CSV")

# Try to import core component
core = None
CORE_COMPONENT_AVAILABLE = False
core_component = None

try:
    # Add the tokenize_backend/src directory to the Python path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'tokenize_backend', 'src'))
    # Import inside a try block to handle import errors gracefully
    import core_component as cc
    core_component = cc
    core = core_component.TokenizationCore()
    CORE_COMPONENT_AVAILABLE = True
    print("Core component initialized successfully")
except ImportError as e:
    print(f"Warning: Could not import core component: {e}")
    CORE_COMPONENT_AVAILABLE = False

class TokenizationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # API endpoints
        if path.startswith('/api/components') or path.startswith('/api/core'):
            self.handle_api_request(path)
        else:
            # Serve static files
            self.serve_static_file(path)
    
    def do_POST(self):
        # Parse the URL
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Handle POST requests for core component
        if path.startswith('/api/core'):
            self.handle_core_post_request(path)
        else:
            self.send_error(404, 'Endpoint not found')
    
    def handle_api_request(self, path):
        # Split path into parts
        parts = path.strip('/').split('/')
        
        # Core component endpoints
        if len(parts) >= 2 and parts[1] == 'core':
            if not CORE_COMPONENT_AVAILABLE or core is None:
                self.send_json_response({
                    'success': False,
                    'data': None,
                    'message': 'Core component not available'
                }, 501)
                return
                
            # /api/core/assets
            if len(parts) == 3 and parts[2] == 'assets':
                if hasattr(core, '_assets'):
                    assets = [asset.to_dict() for asset in core._assets.values()]
                    self.send_json_response({
                        'success': True,
                        'data': assets,
                        'message': None
                    })
                else:
                    self.send_json_response({
                        'success': False,
                        'data': None,
                        'message': 'Core component not properly initialized'
                    }, 500)
            # /api/core/assets/{asset_id}
            elif len(parts) == 4 and parts[2] == 'assets':
                asset_id = urllib.parse.unquote(parts[3])
                if hasattr(core, 'get_asset'):
                    asset = core.get_asset(asset_id)
                    if asset:
                        self.send_json_response({
                            'success': True,
                            'data': asset.to_dict(),
                            'message': None
                        })
                    else:
                        self.send_json_response({
                            'success': False,
                            'data': None,
                            'message': f'Asset not found: {asset_id}'
                        }, 404)
                else:
                    self.send_json_response({
                        'success': False,
                        'data': None,
                        'message': 'Core component not properly initialized'
                    }, 500)
            # /api/core/wallets
            elif len(parts) == 3 and parts[2] == 'wallets':
                if hasattr(core, '_wallets'):
                    wallets = [wallet.to_dict() for wallet in core._wallets.values()]
                    self.send_json_response({
                        'success': True,
                        'data': wallets,
                        'message': None
                    })
                else:
                    self.send_json_response({
                        'success': False,
                        'data': None,
                        'message': 'Core component not properly initialized'
                    }, 500)
            # /api/core/wallets/{wallet_id}
            elif len(parts) == 4 and parts[2] == 'wallets':
                wallet_id = urllib.parse.unquote(parts[3])
                if hasattr(core, 'get_wallet'):
                    wallet = core.get_wallet(wallet_id)
                    if wallet:
                        self.send_json_response({
                            'success': True,
                            'data': wallet.to_dict(),
                            'message': None
                        })
                    else:
                        self.send_json_response({
                            'success': False,
                            'data': None,
                            'message': f'Wallet not found: {wallet_id}'
                        }, 404)
                else:
                    self.send_json_response({
                        'success': False,
                        'data': None,
                        'message': 'Core component not properly initialized'
                    }, 500)
            else:
                self.send_error(404, 'Endpoint not found')
        # Original components endpoints
        elif len(parts) >= 2 and parts[1] == 'components':
            # /api/components
            if len(parts) == 2 and parts[1] == 'components':
                self.send_json_response({
                    'success': True,
                    'data': components,
                    'message': None
                })
            # /api/components/{main_type}
            elif len(parts) == 3 and parts[1] == 'components':
                main_type = urllib.parse.unquote(parts[2])
                filtered = [c for c in components if c['main_type'] == main_type]
                self.send_json_response({
                    'success': True,
                    'data': filtered,
                    'message': None if filtered else f'No components found for type: {main_type}'
                })
            # /api/components/{main_type}/{sub_type}
            elif len(parts) == 4 and parts[1] == 'components':
                main_type = urllib.parse.unquote(parts[2])
                sub_type = urllib.parse.unquote(parts[3])
                filtered = [c for c in components if c['main_type'] == main_type and c['sub_type'] == sub_type]
                self.send_json_response({
                    'success': True,
                    'data': filtered,
                    'message': None if filtered else f'No components found for type: {main_type} and subtype: {sub_type}'
                })
            else:
                self.send_error(404, 'Endpoint not found')
        else:
            self.send_error(404, 'Endpoint not found')
    
    def handle_core_post_request(self, path):
        if not CORE_COMPONENT_AVAILABLE or core is None or core_component is None:
            self.send_json_response({
                'success': False,
                'data': None,
                'message': 'Core component not available'
            }, 501)
            return
            
        # Get the request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_json_response({
                'success': False,
                'data': None,
                'message': 'Invalid JSON'
            }, 400)
            return
        
        # Split path into parts
        parts = path.strip('/').split('/')
        
        # /api/core/assets
        if len(parts) == 3 and parts[2] == 'assets':
            try:
                if hasattr(core_component, 'TokenizedAsset') and hasattr(core, 'create_asset'):
                    # Create a new asset
                    asset_type_str = data.get('asset_type', 'other')
                    
                    asset = core_component.TokenizedAsset(
                        asset_id=data['id'],
                        name=data['name'],
                        asset_type=asset_type_str,
                        value=float(data['value']),
                        owner=data['owner'],
                        metadata=data.get('metadata', {})
                    )
                    
                    asset_id = core.create_asset(asset)
                    self.send_json_response({
                        'success': True,
                        'data': {'id': asset_id},
                        'message': 'Asset created successfully'
                    }, 201)
                else:
                    self.send_json_response({
                        'success': False,
                        'data': None,
                        'message': 'Core component not properly initialized'
                    }, 500)
            except Exception as e:
                self.send_json_response({
                    'success': False,
                    'data': None,
                    'message': f'Error creating asset: {str(e)}'
                }, 400)
        # /api/core/wallets
        elif len(parts) == 3 and parts[2] == 'wallets':
            try:
                if hasattr(core_component, 'DigitalWallet') and hasattr(core, 'create_wallet'):
                    # Create a new wallet
                    wallet_type_str = data.get('wallet_type', 'custodial')
                    
                    wallet = core_component.DigitalWallet(
                        wallet_id=data['id'],
                        owner=data['owner'],
                        wallet_type=wallet_type_str
                    )
                    
                    wallet_id = core.create_wallet(wallet)
                    self.send_json_response({
                        'success': True,
                        'data': {'id': wallet_id},
                        'message': 'Wallet created successfully'
                    }, 201)
                else:
                    self.send_json_response({
                        'success': False,
                        'data': None,
                        'message': 'Core component not properly initialized'
                    }, 500)
            except Exception as e:
                self.send_json_response({
                    'success': False,
                    'data': None,
                    'message': f'Error creating wallet: {str(e)}'
                }, 400)
        else:
            self.send_error(404, 'Endpoint not found')
    
    def serve_static_file(self, path):
        # Default to index.html for root path
        if path == '/' or path == '':
            path = '/index.html'
        
        # Determine file path
        file_path = os.path.join('tokenize_frontend', path.lstrip('/'))
        
        # If file doesn't exist, serve index.html (for SPA)
        if not os.path.exists(file_path):
            file_path = os.path.join('tokenize_frontend', 'index.html')
        
        # Determine content type
        if file_path.endswith('.html'):
            content_type = 'text/html'
        elif file_path.endswith('.js'):
            content_type = 'application/javascript'
        elif file_path.endswith('.css'):
            content_type = 'text/css'
        elif file_path.endswith('.json'):
            content_type = 'application/json'
        else:
            content_type = 'text/plain'
        
        # Serve the file
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(404, f'File not found: {file_path}')
    
    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

# Start server
if __name__ == '__main__':
    PORT = 3032  # Changed from 3030 to avoid conflicts
    
    with socketserver.TCPServer(("", PORT), TokenizationHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print(f"API endpoints available at http://localhost:{PORT}/api/components")
        if CORE_COMPONENT_AVAILABLE:
            print(f"Core component API available at http://localhost:{PORT}/api/core")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")