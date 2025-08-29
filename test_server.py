#!/usr/bin/env python3
"""
簡易HTTPサーバー - CSS変更前後のビジュアルテスト用
ポート8000で起動し、現在のディレクトリをサーブする
"""
import http.server
import socketserver
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # キャッシュを無効化して常に最新のCSSを読み込む
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == "__main__":
    Handler = MyHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()
