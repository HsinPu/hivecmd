"""Team Templates 命令"""
import typer
from rich.console import Console

team_templates_app = typer.Typer(name="templates", help="團隊模板")
console = Console()

@team_templates_app.command("list", help="列出模板")
def list_templates():
    """列出所有模板"""
    from ..team.templates import TemplateManager
    tm = TemplateManager()
    
    templates = tm.list_templates()
    
    console.print("[cyan]可用模板:[/cyan]")
    for t in templates:
        template = tm.get_template(t)
        if template:
            console.print(f"  - {t}: {template.get('description', '-')}")

@team_templates_app.command("show", help="顯示模板詳情")
def show_template(name: str):
    """顯示模板詳情"""
    from ..team.templates import TemplateManager
    tm = TemplateManager()
    
    template = tm.get_template(name)
    if template:
        console.print(f"[cyan]模板: {name}[/cyan]")
        console.print(f"描述: {template.get('description', '-')}")
        console.print("Agent:")
        for agent in template.get("agents", []):
            console.print(f"  - {agent.get('name')}: {agent.get('task')}")
    else:
        console.print(f"[red]模板不存在: {name}[/red]")

@team_templates_app.command("create", help="從模板建立團隊")
def create_from_template(
    template_name: str,
    team_name: str,
    description: str = ""
):
    """從模板建立團隊"""
    try:
        from ..team.templates import TemplateManager
        from ..core.config import Config
        
        tm = TemplateManager()
        template = tm.get_template(template_name)
        
        if not template:
            console.print(f"[red]❌ 模板不存在: {template_name}[/red]")
            return
        
        # 建立團隊
        config = Config()
        config.get_team_dir(team_name)
        
        state = {
            "name": team_name,
            "description": description or template.get("description", ""),
            "status": "active",
            "agents": [],
            "tasks": []
        }
        
        # 加入 template 的 agents
        for agent in template.get("agents", []):
            state["agents"].append({
                "name": agent.get("name"),
                "role": agent.get("role"),
                "task": agent.get("task"),
                "status": "idle"
            })
        
        config.save_state(team_name, state)
        
        console.print(f"[green]✅ 團隊 '{team_name}' 已從模板 '{template_name}' 建立[/green]")
    except Exception as e:
        console.print(f"[red]❌ 建立失敗: {e}[/red]")
