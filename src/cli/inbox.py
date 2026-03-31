"""Inbox 命令 - 訊息收發 (含錯誤處理)"""
import typer
from rich.console import Console
from pathlib import Path
from ..core.config import Config

inbox_app = typer.Typer(name="inbox", help="訊息收發")
console = Console()

@inbox_app.command("send", help="發送訊息")
def send(team: str, to: str, message: str):
    """發送訊息給其他 Agent"""
    try:
        config = Config()
        team_dir = config.get_team_dir(team)
        
        # 確保 inbox 目錄存在
        inbox_dir = team_dir / "inbox"
        inbox_dir.mkdir(exist_ok=True)
        
        # 儲存訊息
        msg_file = inbox_dir / f"{to}.txt"
        with open(msg_file, "a") as f:
            f.write(f"{message}\n")
        
        console.print(f"[green]✅ 訊息已發送給 {to}[/green]")
    except FileNotFoundError:
        console.print(f"[red]❌ 團隊 '{team}' 不存在[/red]")
    except PermissionError:
        console.print(f"[red]❌ 無法寫入訊息，權限不足[/red]")
    except Exception as e:
        console.print(f"[red]❌ 發送失敗: {e}[/red]")

@inbox_app.command("receive", help="接收訊息")
def receive(team: str, agent: str):
    """接收訊息"""
    try:
        config = Config()
        inbox_dir = config.get_team_dir(team) / "inbox"
        msg_file = inbox_dir / f"{agent}.txt"
        
        if not msg_file.exists():
            console.print("[yellow]無新訊息[/yellow]")
            return
        
        with open(msg_file) as f:
            messages = f.read()
        
        console.print(f"[cyan]訊息:[/cyan]\n{messages}")
        
        # 清除已讀
        msg_file.unlink()
    except FileNotFoundError:
        console.print(f"[red]❌ 團隊 '{team}' 不存在[/red]")
    except Exception as e:
        console.print(f"[red]❌ 接收失敗: {e}[/red]")

@inbox_app.command("list", help="列出訊息")
def list_messages(team: str, agent: str = None):
    """列出訊息"""
    try:
        config = Config()
        inbox_dir = config.get_team_dir(team) / "inbox"
        
        if not inbox_dir.exists():
            console.print("[yellow]無訊息[/yellow]")
            return
        
        files = list(inbox_dir.glob("*.txt"))
        if not files:
            console.print("[yellow]無訊息[/yellow]")
            return
        
        console.print(f"[cyan]有 {len(files)} 則訊息:[/cyan]")
        for f in files:
            console.print(f"  - {f.stem}")
    except Exception as e:
        console.print(f"[red]❌ 列出失敗: {e}[/red]")
