"""Leader 命令 - 自動協調 (即時評估 + 串聯)"""
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
    """Leader 會分析任務並串聯執行每個 Agent，即時評估"""
    try:
        config = Config()
        state = config.load_state(team)
        agents = state.get("agents", [])
        
        if not agents:
            console.print("[red]❌ 團隊沒有 Agent[/red]")
            return
        
        agent_names = [a.get("name") for a in agents]
        console.print(f"[cyan]🤖 啟動 Leader: {team}[/cyan]")
        console.print(f"[dim]任務: {task}[/dim]\n")
        
        llm = LLMService()
        
        if not llm.api_key:
            console.print("[red]❌ 請設定 API Key[/red]")
            return
        
        # Leader 規劃
        console.print("[yellow]🤔 Leader 分析任務...[/yellow]")
        
        plan_prompt = f"""你是一個團隊 Leader。你需要分析任務並安排執行順序。

團隊成員: {', '.join(agent_names)}
最終任務: {task}

每個成員的輸出會傳給下一個，請安排能接續工作的順序。
返回 JSON：
{{
    "order": ["成員1", "成員2", ...],
    "tasks": {{"成員1": "任務"}}
}}

只返回 JSON。"""

        plan_result = llm.chat([
            {"role": "system", "content": "你是一個專業的團隊 Leader。"},
            {"role": "user", "content": plan_prompt}
        ])
        
        import re, json
        match = re.search(r'\{[\s\S]*\}', plan_result)
        if match:
            plan = json.loads(match.group())
            order = plan.get("order", agent_names[:3])
            tasks_map = plan.get("tasks", {})
        else:
            order = agent_names[:3]
            tasks_map = {a: f"幫忙完成: {task}" for a in order}
        
        console.print(f"[green]✅ 規劃: {' → '.join(order)}[/green]\n")
        
        # 串聯執行 + 即時評估
        previous_output = ""
        
        for i, agent in enumerate(order):
            console.print(f"\n[yellow]▶ {agent}[/yellow]")
            
            agent_task = tasks_map.get(agent, f"幫忙完成: {task}")
            
            # 加入之前的輸出
            if previous_output:
                execute_prompt = f"""你是 {agent}。請根據以下任務執行：

最終任務: {task}
你的專屬任務: {agent_task}

前面成員的結果:
{previous_output}

請繼續工作並將結果傳給下一個成員。"""
            else:
                execute_prompt = f"""你是 {agent}。請根據以下任務執行：

最終任務: {task}
你的專屬任務: {agent_task}

請執行你的部分。"""

            result = llm.chat([
                {"role": "system", "content": f"你是專業的 {agent}。"},
                {"role": "user", "content": execute_prompt}
            ])
            
            if result:
                console.print(f"[green]✅ 完成[/green]")
                console.print(f"[dim]{result[:80]}...[/dim]")
                
                # 即時評估
                eval_prompt = f"""評估結果是否完成任務：

任務: {task}
{agent} 結果: {result}

回复 "ok" 如果完成，或简短说明需要改进。"""

                eval_result = llm.chat([
                    {"role": "system", "content": "即时评估。"},
                    {"role": "user", "content": eval_prompt}
                ])
                
                if "ok" not in eval_result.lower() or len(eval_result) > 30:
                    console.print(f"[yellow]⚠️ 需改進: {eval_result[:80]}...[/yellow]")
                    
                    # 重新執行
                    retry_prompt = f"""你是 {agent}。結果需要改進：
{eval_result}

任務: {agent_task}
之前的輸出: {previous_output}

請改進。"""

                    retry_result = llm.chat([
                        {"role": "system", "content": f"你是專業的 {agent}。"},
                        {"role": "user", "content": retry_prompt}
                    ])
                    
                    if retry_result:
                        console.print(f"[green]✅ 重新完成[/green]")
                        result = retry_result
                
                # 串聯輸出
                previous_output = result
                
                # 更新狀態
                for a in state.get("agents", []):
                    if a.get("name") == agent:
                        a["status"] = "completed"
                        a["result"] = result
            else:
                console.print(f"[red]❌ 失敗[/red]")
        
        config.save_state(team, state)
        
        console.print(f"\n[green]✅ 全部完成！[/green]")
        
    except Exception as e:
        console.print(f"[red]❌ 錯誤: {e}[/red]")
