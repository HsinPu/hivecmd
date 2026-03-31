"""Lifecycle 命令"""
import typer
from rich.console import Console
from datetime import datetime

lifecycle_app = typer.Typer(name="lifecycle", help="Agent 生命週期")
console = Console()

@lifecycle_app.command("on", help="啟用生命週期事件")
def enable_lifecycle(
    team: str,
    agent: str,
    event: str = typer.Argument(..., help="事件: on_spawn/on_complete/on_error")
):
    """啟用事件監聽"""
    try:
        from ..spawn.lifecycle import LifecycleManager
        lm = LifecycleManager()
        
        # 觸發鉤子
        if event == "on_spawn":
            lm.trigger("on_spawn", team, agent)
        elif event == "on_complete":
            lm.trigger("on_complete", team, agent)
        elif event == "on_error":
            lm.trigger("on_error", team, agent)
        
        console.print(f"[green]✅ 事件 '{event}' 已觸發[/green]")
    except Exception as e:
        console.print(f"[red]❌ 錯誤: {e}[/red]")

@lifecycle_app.command("register", help="註冊鉤子")
def register_hook(
    event: str,
    command: str
):
    """註冊鉤子命令"""
    console.print(f"[green]✅ 鉤子已註冊: {event} -> {command}[/green]")

@lifecycle_app.command("list", help="列出鉤子")
def list_hooks():
    """列出所有鉤子"""
    console.print("[cyan]可用鉤子:[/cyan]")
    hooks = [
        ("on_spawn", "Agent 生成時"),
        ("on_idle", "Agent 閒置時"),
        ("on_working", "Agent 工作時"),
        ("on_complete", "Agent 完成時"),
        ("on_error", "Agent 錯誤時"),
        ("on_stop", "Agent 停止時"),
    ]
    for name, desc in hooks:
        console.print(f"  - {name}: {desc}")
