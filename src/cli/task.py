"""Task 命令 - 任務管理"""
import typer
from rich.console import Console
from ..core.config import Config

task_app = typer.Typer(name="task", help="任務管理")
console = Console()

@task_app.command("list", help="列出任務")
def list_tasks(team: str, owner: str = None):
    """列出團隊任務"""
    config = Config()
    state = config.load_state(team)
    tasks = state.get("tasks", [])
    
    if not tasks:
        console.print("[yellow]無任務[/yellow]")
        return
    
    for t in tasks:
        if owner and t.get("owner") != owner:
            continue
        console.print(f"[cyan]{t.get('id')}[/cyan] {t.get('description')} [{t.get('status')}]")

@task_app.command("update", help="更新任務狀態")
def update(team: str, task_id: str, status: str):
    """更新任務狀態"""
    config = Config()
    state = config.load_state(team)
    tasks = state.get("tasks", [])
    
    for t in tasks:
        if t.get("id") == task_id:
            t["status"] = status
            break
    
    state["tasks"] = tasks
    config.save_state(team, state)
    console.print(f"[green]✅ 任務 {task_id} → {status}[/green]")

@task_app.command("claim", help="認領任務")
def claim(team: str, task_id: str, agent: str):
    """認領任務"""
    config = Config()
    state = config.load_state(team)
    tasks = state.get("tasks", [])
    agents = state.get("agents", [])
    
    for t in tasks:
        if t.get("id") == task_id:
            t["owner"] = agent
            t["status"] = "in_progress"
            break
    
    for a in agents:
        if a.get("name") == agent:
            a["task"] = task_id
            a["status"] = "working"
            break
    
    state["tasks"] = tasks
    state["agents"] = agents
    config.save_state(team, state)
    console.print(f"[green]✅ Agent '{agent}' 認領任務 {task_id}[/green]")
