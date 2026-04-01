"""HiveCmd - Agent Swarm Intelligence CLI"""
import typer
from .cli.team import team_app
from .cli.spawn import spawn_app
from .cli.board import board_app
from .cli.task import task_app
from .cli.inbox import inbox_app
from .cli.preset import preset_app
from .cli.mcp import mcp_app
from .cli.gource import gource_app
from .cli.team_templates import team_templates_app
from .cli.lifecycle import lifecycle_app
from .cli.agent import agent_app
from .cli.pipeline import pipeline_app

app = typer.Typer(name="hivecmd", help="HiveCmd - Agent Swarm Intelligence CLI")

app.add_typer(team_app, name="team")
app.add_typer(spawn_app, name="spawn")
app.add_typer(board_app, name="board")
app.add_typer(task_app, name="task")
app.add_typer(inbox_app, name="inbox")
app.add_typer(preset_app, name="preset")
app.add_typer(mcp_app, name="mcp")
app.add_typer(gource_app, name="gource")
app.add_typer(team_templates_app, name="templates")
app.add_typer(lifecycle_app, name="lifecycle")
app.add_typer(agent_app, name="agent")
app.add_typer(pipeline_app, name="pipeline")

from rich.console import Console
console = Console()

@app.command()
def init():
    from .core.config import Config
    config = Config()
    config.workspace.mkdir(exist_ok=True)
    (config.workspace / "teams").mkdir(exist_ok=True)
    console.print("[green]HiveCmd 初始化完成[/green]")

@app.command()
def status(team: str = None):
    from .core.config import Config
    config = Config()
    if team:
        state = config.load_state(team)
        console.print(f"團隊: {team}")
        console.print(f"  Agents: {len(state.get('agents', []))}")
    else:
        teams = config.list_teams()
        console.print(f"團隊數: {len(teams)}")

if __name__ == "__main__":
    app()
