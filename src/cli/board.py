"""Board 命令 - 監控面板 (完整版)"""
import typer
from rich.console import Console
from rich.table import Table
from ..core.config import Config

board_app = typer.Typer(name="board", help="監控面板")
console = Console()

@board_app.command("show", help="顯示團隊狀態")
def show(team: str = typer.Argument(..., help="團隊名")):
    """顯示團隊即時狀態"""
    config = Config()
    state = config.load_state(team)
    
    console.print(f"\n[bold cyan]📊 {team} 團隊狀態[/bold cyan]\n")
    
    # Agent 表格
    agents = state.get("agents", [])
    if agents:
        table = Table(title="Agents")
        table.add_column("名稱", style="cyan")
        table.add_column("狀態", style="yellow")
        table.add_column("任務", style="blue")
        
        for a in agents:
            table.add_row(
                a.get("name", "-"),
                a.get("status", "idle"),
                a.get("task", "-")[:30] + "..." if a.get("task") else "-"
            )
        console.print(table)
    else:
        console.print("[yellow]無 Agents[/yellow]")
    
    # 任務表格
    tasks = state.get("tasks", [])
    if tasks:
        console.print()
        task_table = Table(title="Tasks")
        task_table.add_column("ID", style="cyan")
        task_table.add_column("描述", style="blue")
        task_table.add_column("狀態", style="green")
        task_table.add_column("負責人", style="yellow")
        
        for t in tasks:
            task_table.add_row(
                t.get("id", "-"),
                t.get("description", "-")[:30],
                t.get("status", "pending"),
                t.get("owner", "-")
            )
        console.print(task_table)
    
    # Tmux 會話
    try:
        from ..spawn.tmux import TmuxManager
        tm = TmuxManager()
        sessions = tm.list_team_sessions(team)
        if sessions:
            console.print(f"\n[dim]Tmux 會話: {', '.join(sessions)}[/dim]")
    except:
        pass

@board_app.command("attach", help="附著到 tmux")
def attach(team: str = typer.Argument(..., help="團隊名")):
    """附著到團隊的 tmux 會話"""
    try:
        from ..spawn.tmux import TmuxManager
        tm = TmuxManager()
        tm.attach_session(team)
    except Exception as e:
        console.print(f"[yellow]無法連接: {e}[/yellow]")

@board_app.command("serve", help="啟動 Web UI")
def serve(port: int = typer.Option(8080, "--port", "-p", help="端口")):
    """啟動 Web 監控面板"""
    try:
        from ..board.web import WebUI
        web = WebUI(port)
        web.start()
    except Exception as e:
        console.print(f"[red]Web UI 啟動失敗: {e}[/red]")
