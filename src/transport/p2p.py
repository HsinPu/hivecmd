"""P2P 傳輸"""
import threading
from rich.console import Console
console = Console()

class P2PTransport:
    """P2P 傳輸層 (簡化版)"""
    
    def __init__(self, port: int = 5555):
        self.port = port
        self.peers = {}
        self.running = False
    
    def start(self):
        """啟動"""
        self.running = True
        console.print(f"[green]🚀 P2P 傳輸啟動: port {self.port}[/green]")
    
    def stop(self):
        """停止"""
        self.running = False
        console.print("[red]🛑 P2P 傳輸已停止[/red]")
    
    def add_peer(self, peer_id: str, address: str):
        """添加 Peer"""
        self.peers[peer_id] = address
        console.print(f"[cyan]➕ Peer: {peer_id}[/cyan]")
    
    def send(self, peer_id: str, message: dict):
        """發送訊息"""
        if peer_id in self.peers:
            console.print(f"[dim]📤 發送給 {peer_id}: {message.get('type')}[/dim]")
