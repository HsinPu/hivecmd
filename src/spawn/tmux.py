"""Tmux 整合 - 為每個 Agent 建立獨立會話"""
import subprocess
from rich.console import Console

console = Console()

class TmuxManager:
    """Tmux 會話管理"""
    
    def __init__(self):
        self.session_prefix = "hivecmd-"
    
    def create_session(self, team: str, agent: str, command: str = None) -> str:
        """建立 tmux 會話"""
        session_name = f"{self.session_prefix}{team}-{agent}"
        
        # 檢查是否已存在
        if self.session_exists(session_name):
            console.print(f"[yellow]⚠️ 會話已存在: {session_name}[/yellow]")
            return session_name
        
        # 建立會話
        cmd = ["tmux", "new-session", "-d", "-s", session_name]
        if command:
            cmd.extend(["-d", command])
        
        subprocess.run(cmd, capture_output=True)
        console.print(f"[green]✅ Tmux 會話: {session_name}[/green]")
        return session_name
    
    def session_exists(self, session_name: str) -> bool:
        """檢查會話是否存在"""
        result = subprocess.run(
            ["tmux", "has-session", "-t", session_name],
            capture_output=True
        )
        return result.returncode == 0
    
    def send_command(self, team: str, agent: str, command: str):
        """發送命令到 tmux 會話"""
        session_name = f"{self.session_prefix}{team}-{agent}"
        subprocess.run(
            ["tmux", "send-keys", "-t", session_name, command, "Enter"],
            capture_output=True
        )
    
    def attach_session(self, team: str):
        """附著到團隊會話"""
        # 列出團隊所有會話
        sessions = self.list_team_sessions(team)
        if sessions:
            # 附著到第一個
            subprocess.run(["tmux", "attach", "-t", sessions[0]])
        else:
            console.print("[yellow]無會話[/yellow]")
    
    def list_team_sessions(self, team: str) -> list:
        """列出團隊所有會話"""
        result = subprocess.run(
            ["tmux", "list-sessions", "-F", "#{session_name}"],
            capture_output=True,
            text=True
        )
        prefix = f"{self.session_prefix}{team}-"
        return [s for s in result.stdout.split("\n") if s.startswith(prefix)]
    
    def kill_session(self, team: str, agent: str = None):
        """結束會話"""
        if agent:
            session_name = f"{self.session_prefix}{team}-{agent}"
            subprocess.run(["tmux", "kill-session", "-t", session_name])
        else:
            # 結束團隊所有會話
            for s in self.list_team_sessions(team):
                subprocess.run(["tmux", "kill-session", "-t", s])
