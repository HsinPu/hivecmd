"""Leader 命令 - AI 自動協調"""
import typer
from rich.console import Console
from ..core.config import Config
from ..services.llm import LLMService

leader_app = typer.Typer(name="leader", help="Leader 自動協調")
console = Console()

@leader_app.command("run", help="啟動 Leader 協調")
def leader_run(
    team: str = typer.Argument(..., help="團隊名"),
    task: str = typer.Option(..., "--task", "-t", help="最終任務")
):
    """Leader 會自動分析任務並協調團隊成員"""
    try:
        config = Config()
        state = config.load_state(team)
        agents = state.get("agents", [])
        
        if not agents:
            console.print("[red]❌ 團隊沒有 Agent[/red]")
            return
        
        agent_names = [a.get("name") for a in agents]
        console.print(f"[cyan]🤖 啟動 Leader: {team}[/cyan]")
        console.print(f"[dim]任務: {task}[/dim]")
        console.print(f"[dim]可用 Agent: {', '.join(agent_names)}[/dim]\n")
        
        llm = LLMService()
        
        if not llm.api_key:
            console.print("[red]❌ 請設定 API Key[/red]")
            return
        
        # Leader 分析並規劃
        console.print("[yellow]🤔 Leader 分析任務...[/yellow]")
        
        plan_prompt = f"""你是一個團隊 Leader。你需要分析任務並決定誰先誰後。

團隊成員: {', '.join(agent_names)}
最終任務: {task}

請規劃執行順序，只選擇需要的成員。返回 JSON 格式：
{{
    "order": ["成員1", "成員2", ...],
    "reason": "簡短說明為什麼這樣安排"
}}

只返回 JSON。"""

        plan_result = llm.chat([
            {"role": "system", "content": "你是一個專業的團隊 Leader，擅長協調任務。"},
            {"role": "user", "content": plan_prompt}
        ])
        
        console.print(f"[green]✅ Leader 規劃完成[/green]")
        console.print(f"[dim]{plan_result[:200]}...[/dim]\n")
        
        # 執行規劃
        console.print("[yellow]▶ 開始執行...[/yellow]")
        
        # 直接讓 Leader 執行完整任務（包含調度）
        execute_prompt = f"""你是一個團隊的 Leader。請執行以下任務：

團隊成員: {', '.join(agent_names)}
最終任務: {task}

你已經分析了任務，請現在直接執行。可以呼叫團隊成員幫忙。

直接開始執行任務，不要問問題。"""

        result = llm.chat([
            {"role": "system", "content": "你是一個專業的 AI Leader，擅長協調團隊完成任務。直接執行，不要問問題。"},
            {"role": "user", "content": execute_prompt}
        ])
        
        console.print(f"\n[green]✅ 執行完成:[/green]")
        console.print(result[:500] if len(result) > 500 else result)
        
        # 更新狀態
        for a in state.get("agents", []):
            a["status"] = "completed"
        config.save_state(team, state)
        
    except Exception as e:
        console.print(f"[red]❌ 錯誤: {e}[/red]")
