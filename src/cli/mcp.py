"""MCP 命令"""
import typer
from rich.console import Console

mcp_app = typer.Typer(name="mcp", help="MCP 伺服器")
console = Console()

@mcp_app.command("start", help="啟動 MCP 伺服器")
def start_server():
    from ..mcp.server import MCPServer
    server = MCPServer()
    server.register_tool("create_team", lambda name: {"status": "ok", "team": name})
    server.register_tool("spawn_agent", lambda **kw: {"status": "ok"})
    console.print("[green]✅ MCP 伺服器啟動中...[/green]")
    console.print("[dim]按 Ctrl+C 停止[/dim]")
    server.run_stdin()

@mcp_app.command("tools", help="列出工具")
def list_tools():
    from ..mcp.server import MCPServer
    server = MCPServer()
    console.print("[cyan]可用工具:[/cyan]")
    for tool in ["create_team", "spawn_agent", "list_teams"]:
        console.print(f"  - {tool}")
