"""配置管理"""
import os
from pathlib import Path
from typing import Optional
import json

class Config:
    """HiveCmd 配置"""
    
    def __init__(self, workspace: Optional[Path] = None):
        self.workspace = workspace or Path.home() / ".hivecmd"
        self.workspace.mkdir(exist_ok=True)
        self.teams_dir = self.workspace / "teams"
        self.teams_dir.mkdir(exist_ok=True)
    
    def get_team_dir(self, team: str) -> Path:
        """取得團隊目錄"""
        d = self.teams_dir / team
        d.mkdir(exist_ok=True)
        return d
    
    def list_teams(self) -> list[str]:
        """列出所有團隊"""
        if not self.teams_dir.exists():
            return []
        return [d.name for d in self.teams_dir.iterdir() if d.is_dir()]
    
    def save_state(self, team: str, state: dict):
        """保存團隊狀態"""
        d = self.get_team_dir(team)
        with open(d / "state.json", "w") as f:
            json.dump(state, f, indent=2)
    
    def load_state(self, team: str) -> dict:
        """載入團隊狀態"""
        d = self.get_team_dir(team)
        f = d / "state.json"
        if f.exists():
            return json.loads(f.read_text())
        return {"name": team, "agents": [], "tasks": []}
