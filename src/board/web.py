"""Web UI - HTTP 監控面板 (完整版)"""
from .server import WebServer
from rich.console import Console

console = Console()

def start_web_ui(port: int = 8080):
    """啟動 Web UI"""
    server = WebServer(port)
    server.start()
    return server
