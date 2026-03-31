"""Git Worktree 整合 - 為每個 Agent 建立獨立分支"""
import subprocess
import os
from pathlib import Path
from rich.console import Console

console = Console()

class WorktreeManager:
    """Git Worktree 管理"""
    
    def __init__(self, base_repo: Path = None):
        self.base_repo = base_repo or Path.cwd()
    
    def create_worktree(self, team: str, agent: str, branch: str = None) -> Path:
        """為 Agent 建立 git worktree"""
        branch = branch or f"agent/{team}/{agent}"
        worktree_path = self.base_repo / ".hivecmd" / "worktrees" / team / agent
        
        try:
            # 建立 worktree
            subprocess.run(
                ["git", "worktree", "add", str(worktree_path), "-b", branch],
                cwd=self.base_repo,
                capture_output=True
            )
            console.print(f"[green]✅ Worktree: {worktree_path}[/green]")
            return worktree_path
        except Exception as e:
            console.print(f"[yellow]⚠️ Worktree 建立失敗: {e}[/yellow]")
            return None
    
    def remove_worktree(self, team: str, agent: str):
        """移除 worktree"""
        worktree_path = self.base_repo / ".hivecmd" / "worktrees" / team / agent
        if worktree_path.exists():
            subprocess.run(
                ["git", "worktree", "remove", "--force", str(worktree_path)],
                cwd=self.base_repo,
                capture_output=True
            )
            console.print(f"[red]🗑️ Worktree 移除: {worktree_path}[/red]")
    
    def list_worktrees(self, team: str = None) -> list:
        """列出 worktrees"""
        worktree_root = self.base_repo / ".hivecmd" / "worktrees"
        if not worktree_root.exists():
            return []
        
        result = []
        for team_dir in worktree_root.iterdir():
            if team and team_dir.name != team:
                continue
            for agent_dir in team_dir.iterdir():
                result.append({
                    "team": team_dir.name,
                    "agent": agent_dir.name,
                    "path": str(agent_dir)
                })
        return result
