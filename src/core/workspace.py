"""工作區管理"""
from pathlib import Path
from typing import Optional
import json

class Workspace:
    """工作區"""
    
    def __init__(self, path: Path):
        self.path = path
        self.config_file = path / ".hivecmd.json"
    
    def exists(self) -> bool:
        return self.path.exists() and self.config_file.exists()
    
    def init(self):
        """初始化工作區"""
        self.path.mkdir(parents=True, exist_ok=True)
        config = {"version": "1.0.0", "teams": []}
        self.config_file.write_text(json.dumps(config, indent=2))
    
    def get_config(self) -> dict:
        """取得配置"""
        if self.config_file.exists():
            return json.loads(self.config_file.read_text())
        return {}
    
    def update_config(self, config: dict):
        """更新配置"""
        self.config_file.write_text(json.dumps(config, indent=2))
    
    def list_teams(self) -> list:
        """列出團隊"""
        return self.get_config().get("teams", [])
    
    def add_team(self, team: str):
        """添加團隊"""
        config = self.get_config()
        teams = config.get("teams", [])
        if team not in teams:
            teams.append(team)
            config["teams"] = teams
            self.update_config(config)
