"""Agent 命令 - AI 自動建立團隊"""
import typer
from rich.console import Console
from rich.progress import Progress
from ..services.llm import LLMService
from ..core.config import Config

agent_app = typer.Typer(name="agent", help="AI 自動建立團隊")
console = Console()

@agent_app.command("create", help="AI 自動建立團隊")
def ai_create(
    request: str = typer.Argument(..., help="需求描述"),
    team_name: str = typer.Option(None, "--team", "-t", help="團隊名稱")
):
    """根據自然語言需求，AI 自動判斷並建立團隊"""
    try:
        # 初始化 LLM
        llm = LLMService()
        
        if not llm.api_key:
            console.print("[red]❌ 請設定 API Key:[/red]")
            console.print("[dim]export HIVECMD_LLM_API_KEY=your-key[/dim]")
            return
        
        console.print(f"[cyan]🤔 分析需求: {request}[/cyan]")
        
        # AI 分析
        config_data = llm.analyze_team_need(request)
        
        team_name = team_name or config_data.get("team_name", "ai-team")
        description = config_data.get("description", "")
        agents_data = config_data.get("agents", [])
        
        console.print(f"\n[green]✅ 建議團隊配置:[/green]")
        console.print(f"  模板: {config_data.get('template', 'custom')}")
        console.print(f"  名稱: {team_name}")
        console.print(f"  描述: {description}")
        console.print(f"  Agents: {len(agents_data)}")
        
        # 建立團隊
        config = Config()
        team_dir = config.get_team_dir(team_name)
        (team_dir / "tasks").mkdir(exist_ok=True)
        (team_dir / "agents").mkdir(exist_ok=True)
        (team_dir / "inbox").mkdir(exist_ok=True)
        
        state = {
            "name": team_name,
            "description": description,
            "status": "active",
            "agents": [],
            "tasks": []
        }
        
        # 加入 AI 推薦的 agents
        for agent in agents_data:
            state["agents"].append({
                "name": agent.get("name"),
                "role": agent.get("role"),
                "task": agent.get("task"),
                "status": "idle"
            })
        
        config.save_state(team_name, state)
        
        console.print(f"\n[green]✅ 團隊 '{team_name}' 建立完成！[/green]")
        console.print(f"[dim]使用 hivecmd board show {team_name} 查看[/dim]")
        
    except Exception as e:
        console.print(f"[red]❌ 錯誤: {e}[/red]")

@agent_app.command("config", help="設定 API")
def config_api(
    api_key: str = typer.Option(..., "--key", "-k", help="API Key"),
    model: str = typer.Option("openai/gpt-4o-mini", "--model", "-m", help="模型")
):
    """設定 API Key"""
    import os
    os.environ["HIVECMD_LLM_API_KEY"] = api_key
    os.environ["HIVECMD_LLM_MODEL"] = model
    console.print(f"[green]✅ API 已設定: {model}[/green]")
