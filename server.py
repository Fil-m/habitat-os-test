#!/usr/bin/env python3
"""Habitat OS — local dev server (GitHub-powered market sync)"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]} {args[1]}")

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    print(f"\n{'='*45}")
    print(f"  🚀 HABITAT OS — Dev Server")
    print(f"  📍 http://localhost:{PORT}")
    print(f"  📱 http://10.198.21.43:{PORT}")
    print(f"  🌐 Market: GitHub API (no local server needed)")
    print(f"{'='*45}\n")
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    try: server.serve_forever()
    except KeyboardInterrupt: print("\nServer stopped.")
