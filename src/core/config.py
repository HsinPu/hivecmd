"""配置管理 (含類型註解)"""
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
import json

class Config:
    """HiveCmd 配置"""
    
    def __init__(self, workspace: Optional[Path] = None) -> None:
        self.workspace: Path = workspace or Path.home() / ".hivecmd"
        self.workspace.mkdir(exist_ok=True)
        self.teams_dir: Path = self.workspace / "teams"
        self.teams_dir.mkdir(exist_ok=True)
    
    def get_team_dir(self, team: str) -> Path:
        """取得團隊目錄"""
        d = self.teams_dir / team
        d.mkdir(exist_ok=True)
        return d
    
    def list_teams(self) -> List[str]:
        """列出所有團隊"""
        if not self.teams_dir.exists():
            return []
        return [d.name for d in self.teams_dir.iterdir() if d.is_dir()]
    
    def save_state(self, team: str, state: Dict[str, Any]) -> None:
        """保存團隊狀態"""
        d = self.get_team_dir(team)
        with open(d / "state.json", "w") as f:
            json.dump(state, f, indent=2)
    
    def load_state(self, team: str) -> Dict[str, Any]:
        """載入團隊狀態"""
        d = self.get_team_dir(team)
        f = d / "state.json"
        if f.exists():
            return json.loads(f.read_text())
        return {"name": team, "agents": [], "tasks": []}
    
    def delete_team(self, team: str) -> bool:
        """刪除團隊"""
        d = self.get_team_dir(team)
        if d.exists():
            import shutil
            shutil.rmtree(d)
            return True
        return False
