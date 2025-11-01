#!/usr/bin/env python3
import http.server
import socketserver
import json
import csv
import urllib.parse
from http.server import BaseHTTPRequestHandler
import os

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

class TokenizationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # API endpoints
        if path.startswith('/api/components'):
            self.handle_api_request(path)
        else:
            # Serve static files
            self.serve_static_file(path)
    
    def handle_api_request(self, path):
        # Split path into parts
        parts = path.strip('/').split('/')
        
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
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

# Start server
if __name__ == '__main__':
    PORT = 3031  # Changed from 3030 to avoid conflicts
    
    with socketserver.TCPServer(("", PORT), TokenizationHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print(f"API endpoints available at http://localhost:{PORT}/api/components")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")