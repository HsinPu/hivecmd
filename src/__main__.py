"""HiveCmd - Agent Swarm Intelligence CLI"""
import typer
from rich.console import Console
from rich import print
from .cli.team import team_app
from .cli.spawn import spawn_app
from .cli.board import board_app
from .cli.task import task_app
from .cli.inbox import inbox_app

app = typer.Typer(
    name="hivecmd",
    help="""[bold cyan]HiveCmd[/bold cyan] - Agent Swarm Intelligence CLI
    
    [yellow]範例:[/yellow]
      hivecmd team create my-team
      hivecmd spawn agent my-team --name worker1 --task "implement auth"
      hivecmd board show my-team
    """,
    
)

# 註冊子命令
app.add_typer(team_app, name="team")
app.add_typer(spawn_app, name="spawn")
app.add_typer(board_app, name="board")
app.add_typer(task_app, name="task")
app.add_typer(inbox_app, name="inbox")

console = Console()

@app.command()
def init():
    """初始化 HiveCmd"""
    from pathlib import Path
    from .core.config import Config
    
    config = Config()
    console.print(f"[green]✅ HiveCmd 初始化完成[/green]")
    console.print(f"[dim]工作目錄: {config.workspace}[/dim]")

@app.command()
def status(team: str = typer.Argument(None, help="團隊名")):
    """顯示狀態"""
    from .core.config import Config
    
    config = Config()
    if team:
        state = config.load_state(team)
        console.print(f"\n[cyan]團隊: {team}[/cyan]")
        console.print(f"  Agents: {len(state.get('agents', []))}")
        console.print(f"  Tasks: {len(state.get('tasks', []))}")
    else:
        teams = config.list_teams()
        console.print(f"[cyan]團隊數: {len(teams)}[/cyan]")
        for t in teams:
            state = config.load_state(t)
            console.print(f"  - {t} ({len(state.get('agents', []))} agents)")

# 設定預設命令
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """HiveCmd - Agent Swarm Intelligence"""
    if ctx.invoked_subcommand is None:
        console.print("[bold cyan]HiveCmd v1.0.0[/bold cyan] - Agent Swarm Intelligence CLI")
        console.print("[dim]使用 --help 查看命令[/dim]")

if __name__ == "__main__":
    app()
