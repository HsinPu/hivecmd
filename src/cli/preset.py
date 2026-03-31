"""Preset 命令"""
import typer
from rich.console import Console

preset_app = typer.Typer(name="preset", help="預設配置")
console = Console()

@preset_app.command("list", help="列出預設")
def list_presets():
    from ..config.preset import PresetManager
    pm = PresetManager()
    presets = pm.list_presets()
    console.print("[cyan]可用預設:[/cyan]")
    for p in presets:
        console.print(f"  - {p}")

@preset_app.command("use", help="使用預設")
def use_preset(name: str):
    from ..config.preset import PresetManager
    pm = PresetManager()
    if pm.use_preset(name):
        console.print(f"[green]✅ 已切換到 {name}[/green]")
    else:
        console.print(f"[red]❌ 預設不存在: {name}[/red]")

@preset_app.command("show", help="顯示預設")
def show_preset(name: str):
    from ..config.preset import PresetManager
    pm = PresetManager()
    preset = pm.get_preset(name)
    if preset:
        import json
        console.print(json.dumps(preset, indent=2))
    else:
        console.print(f"[red]預設不存在: {name}[/red]")
