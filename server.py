#!/usr/bin/env python3
"""Habitat OS — local test server with shared API"""
import json, os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

PORT = 8000
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mockups_data')
os.makedirs(DATA_DIR, exist_ok=True)
MARKET_FILE = os.path.join(DATA_DIR, 'market.json')
PROFILES_FILE = os.path.join(DATA_DIR, 'profiles.json')
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default
def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        p = urlparse(self.path).path
        if p == '/api/market/listings':
            self.send_json(load_json(MARKET_FILE, []))
        elif p == '/api/profiles/list':
            self.send_json(load_json(PROFILES_FILE, []))
        else:
            super().do_GET()
    
    def do_POST(self):
        p = urlparse(self.path).path
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        
        if p == '/api/market/list':
            listings = load_json(MARKET_FILE, [])
            body['id'] = 'm_' + str(int(__import__('time').time()))
            body['listed_at'] = __import__('datetime').datetime.now().isoformat()
            listings.append(body)
            save_json(MARKET_FILE, listings)
            self.send_json({"ok": True, "listings": listings})
        
        elif p == '/api/market/buy':
            listing_id = body.get('id')
            buyer = body.get('buyer')
            listings = load_json(MARKET_FILE, [])
            new_listings = [l for l in listings if l['id'] != listing_id]
            bought = None
            for l in listings:
                if l['id'] == listing_id:
                    bought = l
                    break
            if bought:
                # Add to buyer's profile (notified on next load)
                save_json(MARKET_FILE, new_listings)
                self.send_json({"ok": True, "bought": bought})
            else:
                self.send_json({"ok": False, "error": "Not found"}, 404)
        
        elif p == '/api/market/remove':
            listing_id = body.get('id')
            listings = load_json(MARKET_FILE, [])
            listings = [l for l in listings if l['id'] != listing_id]
            save_json(MARKET_FILE, listings)
            self.send_json({"ok": True})
        
        elif p == '/api/profiles/register':
            profiles = load_json(PROFILES_FILE, [])
            existing = [pr for pr in profiles if pr['id'] == body.get('id')]
            if not existing:
                profiles.append(body)
                save_json(PROFILES_FILE, profiles)
            self.send_json({"ok": True, "profiles": profiles})
        
        else:
            self.send_json({"error": "unknown"}, 404)
    
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]} {args[1]}")

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    print(f"\n{'='*45}")
    print(f"  🚀 HABITAT OS — Local Test Server")
    print(f"  📍 http://localhost:{PORT}")
    print(f"  📱 http://10.198.21.43:{PORT}")
    print(f"  🌐 Shared API: market, profiles")
    print(f"{'='*45}\n")
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    try: server.serve_forever()
    except KeyboardInterrupt: print("\nServer stopped.")
