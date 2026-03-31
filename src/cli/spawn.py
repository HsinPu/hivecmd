"""Spawn 命令 - 生成 Agent"""
import typer
from rich.console import Console
from ..core.config import Config
from ..core.identity import AgentIdentity
import uuid

spawn_app = typer.Typer(name="spawn", help="生成 Worker Agent")
console = Console()

@spawn_app.command("agent", help="生成 Agent")
def spawn_agent(
    team: str = typer.Argument(..., help="團隊名"),
    name: str = typer.Option(None, "--name", "-n", help="Agent 名稱"),
    task: str = typer.Option("", "--task", "-t", help="任務描述"),
    agent_type: str = typer.Option("claude", "--type", help="Agent 類型")
):
    """生成 Worker Agent"""
    config = Config()
    state = config.load_state(team)
    
    # 生成 Agent ID
    agent_id = name or f"agent-{len(state.get('agents', [])) + 1}"
    
    # 建立 Agent 身份
    identity = AgentIdentity(
        name=agent_id,
        team=team,
        role="worker",
        status="active",
        task=task
    )
    
    # 保存 Agent
    agents = state.get("agents", [])
    agents.append(identity.to_dict())
    state["agents"] = agents
    config.save_state(team, state)
    
    console.print(f"[green]✅ Agent '{agent_id}' 已生成[/green]")
    console.print(f"[dim]團隊: {team} | 任務: {task or '無'}[/dim]")

@spawn_app.command("task", help="生成任務")
def spawn_task(
    team: str = typer.Argument(..., help="團隊名"),
    description: str = typer.Option(..., "--task", "-t", help="任務描述"),
    blocked_by: str = typer.Option(None, help="依賴任務 ID")
):
    """生成任務"""
    config = Config()
    state = config.load_state(team)
    
    # 生成任務 ID
    task_id = f"task-{len(state.get('tasks', [])) + 1}"
    
    task = {
        "id": task_id,
        "description": description,
        "status": "pending",
        "blocked_by": blocked_by,
        "owner": None
    }
    
    tasks = state.get("tasks", [])
    tasks.append(task)
    state["tasks"] = tasks
    config.save_state(team, state)
    
    console.print(f"[green]✅ 任務 '{task_id}' 已建立[/green]")
    console.print(f"[dim]描述: {description}[/dim]")
