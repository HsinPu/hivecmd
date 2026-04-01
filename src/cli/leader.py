"""Leader 命令 - 自動協調"""
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
    """Leader 會分析任務並分配給團隊成員執行"""
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

請規劃執行順序。返回 JSON 格式：
{{
    "order": ["成員1", "成員2", ...],
    "tasks": {{
        "成員1": "這個成員的具體任務",
        "成員2": "這個成員的具體任務"
    }}
}}

只返回 JSON。"""

        plan_result = llm.chat([
            {"role": "system", "content": "你是一個專業的團隊 Leader，擅長協調任務。"},
            {"role": "user", "content": plan_prompt}
        ])
        
        # 解析規劃
        import re, json
        match = re.search(r'\{[\s\S]*\}', plan_result)
        if match:
            plan = json.loads(match.group())
            order = plan.get("order", agent_names[:3])
            tasks_map = plan.get("tasks", {})
        else:
            order = agent_names[:3]
            tasks_map = {a: f"幫忙完成任務: {task}" for a in order}
        
        console.print(f"[green]✅ 規劃完成: {' → '.join(order)}[/green]\n")
        
        # 執行規劃 - 真的呼叫每個 Agent
        for i, agent in enumerate(order):
            console.print(f"\n[yellow]▶ 第 {i+1}/{len(order)}: {agent}[/yellow]")
            
            agent_task = tasks_map.get(agent, f"幫忙完成: {task}")
            
            # 呼叫對應的 Agent 執行任務
            # 這裡我們用 LLM 模擬那個 Agent 執行
            execute_prompt = f"""你是 {agent}。請根據以下任務執行：

最終任務: {task}
你的專屬任務: {agent_task}

請執行你的部分工作。"""

            result = llm.chat([
                {"role": "system", "content": f"你是一個專業的 {agent}。"},
                {"role": "user", "content": execute_prompt}
            ])
            
            if result:
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
        
        console.print(f"\n[green]✅ 全部完成！[/green]")
        console.print(f"[dim]共 {len(order)} 個 Agent 已執行[/dim]")
        
    except Exception as e:
        console.print(f"[red]❌ 錯誤: {e}[/red]")
