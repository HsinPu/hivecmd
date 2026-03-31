"""Web UI 伺服器"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
import threading

class HiveCmdHandler(BaseHTTPRequestHandler):
    """HTTP 請求處理"""
    
    def do_GET(self):
        path = urlparse(self.path).path
        
        # API endpoints
        if path == "/api/status":
            self.send_json({"status": "ok", "version": "1.0.0"})
        elif path == "/api/teams":
            from ..core.config import Config
            config = Config()
            teams = config.list_teams()
            self.send_json(teams)
        elif path.startswith("/api/team/"):
            team_name = path.split("/")[-1]
            from ..core.config import Config
            config = Config()
            state = config.load_state(team_name)
            self.send_json(state)
        elif path == "/api/version":
            self.send_json({"version": "1.0.0"})
        else:
            # 靜態檔案
            self.send_response(404)
            self.end_headers()
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        pass  # 抑制日誌

class WebServer:
    """Web 伺服器"""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.server = None
    
    def start(self):
        self.server = HTTPServer(("", self.port), HiveCmdHandler)
        print(f"🌐 Web UI: http://localhost:{self.port}")
        thread = threading.Thread(target=self.server.serve_forever)
        thread.daemon = True
        thread.start()
    
    def stop(self):
        if self.server:
            self.server.shutdown()
            print("🛑 Web Server stopped")
