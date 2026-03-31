"""團隊複製"""
import shutil
from pathlib import Path
from rich.console import Console

console = Console()

class TeamCloner:
    """團隊複製器"""
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
    
    def clone(self, source_team: str, target_team: str) -> bool:
        """複製團隊"""
        source = self.workspace / "teams" / source_team
        target = self.workspace / "teams" / target_team
        
        if not source.exists():
            console.print(f"[red]來源團隊不存在: {source_team}[/red]")
            return False
        
        try:
            shutil.copytree(source, target)
            console.print(f"[green]✅ 團隊已複製: {source_team} → {target_team}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]複製失敗: {e}[/red]")
            return False
    
    def export_template(self, team: str, output: Path) -> bool:
        """匯出為模板"""
        source = self.workspace / "teams" / team
        if not source.exists():
            return False
        
        # 只匯出任務結構，不含狀態
        import json
        state_file = source / "state.json"
        if state_file.exists():
            state = json.loads(state_file.read_text())
            # 移除 agents 狀態
            template = {
                "name": team,
                "tasks": state.get("tasks", [])
            }
            output.write_text(json.dumps(template, indent=2))
            return True
        return False
