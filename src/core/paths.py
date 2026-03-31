"""路徑管理"""
from pathlib import Path
from typing import Optional
import os

class PathManager:
    """路徑管理器"""
    
    def __init__(self, workspace: Optional[Path] = None):
        self.workspace = workspace or Path.home() / ".hivecmd"
        self.teams = self.workspace / "teams"
        self.worktrees = self.workspace / "worktrees"
        self.cache = self.workspace / "cache"
        self.logs = self.workspace / "logs"
    
    def ensure_all(self):
        """確保所有目錄存在"""
        for d in [self.workspace, self.teams, self.worktrees, self.cache, self.logs]:
            d.mkdir(parents=True, exist_ok=True)
    
    def get_team_dir(self, team: str) -> Path:
        return self.teams / team
    
    def get_worktree_dir(self, team: str, agent: str) -> Path:
        return self.worktrees / team / agent
    
    def get_agent_log(self, team: str, agent: str) -> Path:
        return self.logs / f"{team}-{agent}.log"
