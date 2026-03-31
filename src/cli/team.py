"""Team 命令 - 團隊管理"""
import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
import subprocess
from ..core.config import Config

team_app = typer.Typer(name="team", help="團隊管理")
console = Console()

@team_app.command("create", help="建立團隊")
def create(name: str, description: str = typer.Option("", "--description", "-d", help="描述")):
    """建立新團隊"""
    config = Config()
    team_dir = config.get_team_dir(name)
    
    # 建立團隊目錄結構
    (team_dir / "tasks").mkdir(exist_ok=True)
    (team_dir / "agents").mkdir(exist_ok=True)
    (team_dir / "inbox").mkdir(exist_ok=True)
    
    # 初始化狀態
    state = {
        "name": name,
        "description": description,
        "status": "active",
        "agents": [],
        "tasks": []
    }
    config.save_state(name, state)
    
    console.print(f"[green]✅ 團隊 '{name}' 建立完成[/green]")
    console.print(f"[dim]團隊目錄: {team_dir}[/dim]")

@team_app.command("list", help="列出團隊")
def list_teams():
    """列出所有團隊"""
    config = Config()
    teams = config.list_teams()
    
    if not teams:
        console.print("[yellow]尚無團隊[/yellow]")
        return
    
    table = Table(title="團隊列表")
    table.add_column("名稱", style="cyan")
    table.add_column("狀態", style="green")
    table.add_column("Agent 數", style="blue")
    
    for t in teams:
        state = config.load_state(t)
        table.add_row(t, state.get("status", "active"), str(len(state.get("agents", []))))
    
    console.print(table)

@team_app.command("delete", help="刪除團隊")
def delete(name: str, force: bool = False):
    """刪除團隊"""
    if not force:
        console.print(f"[red]確認刪除團隊 '{name}'？使用 --force 強制刪除[/red]")
        return
    
    import shutil
    config = Config()
    team_dir = config.get_team_dir(name)
    if team_dir.exists():
        shutil.rmtree(team_dir)
    console.print(f"[green]✅ 團隊 '{name}' 已刪除[/green]")

@team_app.command("show", help="顯示團隊詳情")
def show(name: str):
    """顯示團隊詳情"""
    config = Config()
    state = config.load_state(name)
    
    console.print(f"\n[bold cyan]團隊: {name}[/bold cyan]")
    console.print(f"描述: {state.get('description', '-')}")
    console.print(f"狀態: {state.get('status', 'active')}")
    console.print(f"Agent 數: {len(state.get('agents', []))}")
    console.print(f"任務數: {len(state.get('tasks', []))}")
