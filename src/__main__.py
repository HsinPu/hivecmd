"""HiveCmd - Agent Swarm Intelligence CLI"""
import typer
from rich.console import Console

app = typer.Typer(name="hivecmd", help="HiveCmd - Agent Swarm Intelligence CLI")
console = Console()

@app.command()
def init():
    """初始化專案"""
    console.print("[green]HiveCmd 初始化完成！[/green]")

@app.command()
def team(name: str):
    """團隊管理"""
    console.print(f"[blue]團隊: {name}[/blue]")

@app.command()
def spawn(team: str, agent: str, task: str):
    """生成 Worker Agent"""
    console.print(f"[green]生成 {agent} → {task}[/green]")

@app.command()
def board(action: str = "attach", team: str = ""):
    """監控面板"""
    console.print(f"[yellow]Board: {action} {team}[/yellow]")

if __name__ == "__main__":
    app()
