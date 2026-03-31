"""Gource 命令"""
import typer
from rich.console import Console
from pathlib import Path

gource_app = typer.Typer(name="gource", help="Gource 可視化")
console = Console()

@gource_app.command("run", help="執行 Gource 可視化")
def run_gource(
    repo: str = typer.Argument(".", help="Repo 路徑"),
    seconds: int = typer.Option(60, "--seconds", "-s", help="秒數")
):
    """執行 Gource"""
    try:
        from ..board.gource import GourceRenderer
        r = GourceRenderer(Path(repo))
        
        # 產生範例日誌
        events = [
            {"action": "A", "path": "/src/main.py", "user": "hivecmd"},
            {"action": "A", "path": "/src/config.py", "user": "hivecmd"},
            {"action": "M", "path": "/src/main.py", "user": "hivecmd"},
        ]
        r.generate_log(events)
        
        success = r.run()
        if success:
            console.print(f"[green]✅ Gource 可視化完成[/green]")
        else:
            console.print("[yellow]⚠️ 請安裝 gource: sudo apt install gource[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ 錯誤: {e}[/red]")

@gource_app.command("export", help="匯出影片")
def export_video(
    repo: str = typer.Argument(".", help="Repo 路徑"),
    output: str = typer.Option("gource.mp4", "--output", "-o", help="輸出檔案")
):
    """匯出 Gource 影片"""
    try:
        from ..board.gource import GourceRenderer
        r = GourceRenderer(Path(repo))
        
        events = [
            {"action": "A", "path": "/src/main.py", "user": "hivecmd"},
        ]
        r.generate_log(events)
        
        success = r.export_video(output)
        if success:
            console.print(f"[green]✅ 已匯出: {output}[/green]")
        else:
            console.print("[red]❌ 匯出失敗，請安裝 ffmpeg[/red]")
    except Exception as e:
        console.print(f"[red]❌ 錯誤: {e}[/red]")
