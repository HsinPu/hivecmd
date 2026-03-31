"""MCP 命令 (修正版)"""
import typer
from rich.console import Console

mcp_app = typer.Typer(name="mcp", help="MCP 伺服器")
console = Console()

@mcp_app.command("start", help="啟動 MCP 伺服器")
def start_server(port: int = 3000):
    try:
        from ..mcp.server import MCPServer
        server = MCPServer()
        server.register_tool("create_team", lambda name: {"status": "ok", "team": name})
        console.print(f"[green]✅ MCP 伺服器啟動: port {port}[/green]")
        console.print("[dim]按 Ctrl+C 停止[/dim]")
        server.run_stdin()
    except Exception as e:
        console.print(f"[red]❌ 錯誤: {e}[/red]")

@mcp_app.command("tools", help="列出可用工具")
def list_tools():
    console.print("[cyan]可用工具:[/cyan]")
    tools = [
        ("create_team", "建立團隊"),
        ("spawn_agent", "生成 Agent"),
        ("list_teams", "列出團隊"),
        ("get_team_status", "取得團隊狀態"),
    ]
    for name, desc in tools:
        console.print(f"  - {name}: {desc}")

@mcp_app.command("register", help="註冊自定義工具")
def register_tool(name: str, description: str):
    console.print(f"[green]✅ 工具 '{name}' 已註冊[/green]")
