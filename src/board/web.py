"""Web UI - HTTP 監控面板"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from pathlib import Path
from threading import Thread
from rich.console import Console

console = Console()

class WebUI:
    """Web UI 伺服器"""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.running = False
    
    def start(self):
        """啟動 Web UI"""
        self.running = True
        
        # 簡單的 HTTP 處理器
        class Handler(SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/api/status":
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "ok"}).encode())
                else:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"<html><body><h1>HiveCmd Web UI</h1></body></html>")
            
            def log_message(self, format, *args):
                pass  # 抑制日誌
        
        server = HTTPServer(("", self.port), Handler)
        
        console.print(f"[green]🌐 Web UI: http://localhost:{self.port}[/green]")
        
        # 非阻塞啟動
        thread = Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
    
    def stop(self):
        """停止 Web UI"""
        self.running = False
        console.print("[red]🛑 Web UI 已停止[/red]")
