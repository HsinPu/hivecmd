"""Pipeline 命令 - 自動協調 Agent"""
import typer
from rich.console import Console
from rich.progress import Progress
from ..core.config import Config
from ..services.llm import LLMService

pipeline_app = typer.Typer(name="pipeline", help="自動協調 Agent")
console = Console()

@pipeline_app.command("run", help="執行 Pipeline")
def run_pipeline(
    team: str = typer.Argument(..., help="團隊名"),
    agents: str = typer.Option(..., "--agents", "-a", help="Agent 名稱 (逗號分隔)"),
    task: str = typer.Option(..., "--task", "-t", help="最終任務")
):
    """自動協調多個 Agent 順序執行"""
    try:
        agent_list = [a.strip() for a in agents.split(",")]
        
        console.print(f"[cyan]🤖 啟動 Pipeline: {team}[/cyan]")
        console.print(f"[dim]執行順序: {' → '.join(agent_list)}[/dim]")
        console.print(f"[dim]任務: {task}[/dim]\n")
        
        llm = LLMService()
        
        if not llm.api_key:
            console.print("[red]❌ 請設定 API Key:[/red]")
            console.print("[dim]export HIVECMD_LLM_API_KEY=your-key[/dim]")
            return
        
        config = Config()
        state = config.load_state(team)
        
        results = {}
        
        for i, agent in enumerate(agent_list):
            console.print(f"\n[yellow]▶ 第 {i+1}/{len(agent_list)} 步: {agent}[/yellow]")
            
            # 構建 context
            context = ""
            if results:
                context = "\n\n之前完成的內容:\n" + "\n".join([f"- {k}: {v[:200]}..." for k, v in results.items()])
            
            prompt = f"""你是 {agent}。請根據以下任務執行工作：

最終任務: {task}
你的角色: {agent}

{context}

請直接執行你的部分工作，完成後簡短回報結果。"""
            
            result = llm.chat([
                {"role": "system", "content": "你是一個專業的 AI Agent，擅長團隊協作。"},
                {"role": "user", "content": prompt}
            ])
            
            if result:
                results[agent] = result
                console.print(f"[green]✅ {agent} 完成[/green]")
                console.print(f"[dim]{result[:150]}...[/dim]")
                
                # 更新 Agent 狀態
                for a in state.get("agents", []):
                    if a.get("name") == agent:
                        a["status"] = "completed"
                        a["result"] = result
            else:
                console.print(f"[red]❌ {agent} 失敗[/red]")
        
        config.save_state(team, state)
        
        console.print(f"\n[green]✅ Pipeline 完成！[/green]")
        console.print(f"[dim]共 {len(results)} 個 Agent 執行完成[/dim]")
        
    except Exception as e:
        console.print(f"[red]❌ 錯誤: {e}[/red]")
