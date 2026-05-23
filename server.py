#!/usr/bin/env python3
"""Simple HTTP server for Habitat OS local testing."""
import http.server
import socketserver
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]} {args[1]} {args[2]}")

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    print(f"Habitat OS server running at http://localhost:{PORT}")
    print(f"Serving files from: {DIRECTORY}")
    print("Press Ctrl+C to stop.")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            httpd.shutdown()
