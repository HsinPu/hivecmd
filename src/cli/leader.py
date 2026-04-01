"""Leader 命令 - 自動協調 (实时评估)"""
import typer
from rich.console import Console
from ..core.config import Config
from ..services.llm import LLMService

leader_app = typer.Typer(name="leader", help="Leader 自動協調")
console = Console()

@leader_app.command("run", help="啟動 Leader 協調")
def leader_run(
    team: str = typer.Argument(..., help="團隊名"),
    task: str = typer.Option(..., "--task", "-t", help="最終任務"),
    max_loops: int = typer.Option(3, "--max-loops", "-l", help="最大迴圈次數")
):
    """Leader 會分析任務並分配給團隊成員執行，每個執行完立即評估"""
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
        
        loop_count = 0
        execution_count = 0
        
        while loop_count < max_loops:
            loop_count += 1
            console.print(f"\n[cyan]=== 迴圈 {loop_count}/{max_loops} ===[/cyan]")
            
            # Leader 規劃
            console.print("[yellow]🤔 Leader 分析任務...[/yellow]")
            
            plan_prompt = f"""你是一個團隊 Leader。你需要分析任務並決定誰先誰後。

團隊成員: {', '.join(agent_names)}
最終任務: {task}

請規劃執行順序。返回 JSON：
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
                tasks_map = {a: f"幫忙: {task}" for a in order}
            
            console.print(f"[green]✅ 規劃: {' → '.join(order)}[/green]\n")
            
            # 執行並即时评估
            for i, agent in enumerate(order):
                execution_count += 1
                console.print(f"\n[yellow]▶ [{execution_count}] {agent}[/yellow]")
                
                agent_task = tasks_map.get(agent, f"幫忙: {task}")
                
                execute_prompt = f"""你是 {agent}。請執行：

任務: {agent_task}"""

                result = llm.chat([
                    {"role": "system", "content": f"你是專業的 {agent}。"},
                    {"role": "user", "content": execute_prompt}
                ])
                
                if result:
                    console.print(f"[green]✅ {agent} 完成[/green]")
                    console.print(f"[dim]{result[:80]}...[/dim]")
                    
                    # ===== 即时评估 =====
                    eval_prompt = f"""評估以下結果是否完成任務：

任務: {task}
{agent} 的結果: {result}

回复 "ok" 表示完成，或简短说明需要改进的地方。"""

                    eval_result = llm.chat([
                        {"role": "system", "content": "你是 Leader，即时评估结果。"},
                        {"role": "user", "content": eval_prompt}
                    ])
                    
                    if "ok" in eval_result.lower() and len(eval_result) < 30:
                        console.print(f"[green]✓ 評估通過[/green]")
                    else:
                        console.print(f"[yellow]⚠️ 需要改進: {eval_result[:100]}...[/yellow]")
                        
                        # 立即重新執行
                        console.print(f"[yellow]🔄 重新執行 {agent}...[/yellow]")
                        
                        retry_prompt = f"""你是 {agent}。之前的結果不夠好：

{eval_result}

請重新執行任務，改进上述问题。"""

                        retry_result = llm.chat([
                            {"role": "system", "content": f"你是專業的 {agent}。"},
                            {"role": "user", "content": retry_prompt}
                        ])
                        
                        if retry_result:
                            console.print(f"[green]✅ {agent} 重新完成[/green]")
                            result = retry_result
                    
                    # 更新狀態
                    for a in state.get("agents", []):
                        if a.get("name") == agent:
                            a["status"] = "completed"
                            a["result"] = result
                else:
                    console.print(f"[red]❌ {agent} 失敗[/red]")
            
            config.save_state(team, state)
            
            # 最後评估
            if loop_count < max_loops:
                final_eval = llm.chat([
                    {"role": "system", "content": "评估整体结果。"},
                    {"role": "user", "content": f"任务: {task}. 回复 'ok' 如果完成。"}
                ])
                
                if "ok" in final_eval.lower() and len(final_eval) < 30:
                    console.print(f"\n[green]✅ 全部完成！共 {execution_count} 次執行[/green]")
                    break
        
        console.print(f"\n[yellow]⚠️ 完成 ({execution_count} 次執行)[/yellow]")
        
    except Exception as e:
        console.print(f"[red]❌ 錯誤: {e}[/red]")
