"""Leader 命令 - 自動協調 (含回溯)"""
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
    """Leader 會分析任務並分配給團隊成員執行，支援回溯"""
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
        console.print(f"[dim]最大迴圈: {max_loops}[/dim]\n")
        
        llm = LLMService()
        
        if not llm.api_key:
            console.print("[red]❌ 請設定 API Key[/red]")
            return
        
        # 追蹤執行歷史
        execution_history = []
        loop_count = 0
        
        while loop_count < max_loops:
            loop_count += 1
            console.print(f"\n[cyan]=== 迴圈 {loop_count}/{max_loops} ===[/cyan]")
            
            # Leader 分析並規劃
            console.print("[yellow]🤔 Leader 分析任務...[/yellow]")
            
            # 如果有歷史，加入 context
            history_context = ""
            if execution_history:
                history_context = "\n\n之前的執行記錄:\n"
                for h in execution_history[-3:]:  # 只顯示最近3個
                    history_context += f"- {h['agent']}: {h['result'][:100]}...\n"
                history_context += "\n如果之前的結果不好，請指出哪個 Agent 需要重新執行。"
            
            plan_prompt = f"""你是一個團隊 Leader。你需要分析任務並決定誰先誰後。

團隊成員: {', '.join(agent_names)}
最終任務: {task}
{history_context}

請規劃執行順序。返回 JSON 格式：
{{
    "order": ["成員1", "成員2", ...],
    "tasks": {{"成員1": "任務", "成員2": "任務"}},
    "feedback": "對之前的評估，或空字串"
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
                feedback = plan.get("feedback", "")
            else:
                order = agent_names[:3]
                tasks_map = {a: f"幫忙完成: {task}" for a in order}
                feedback = ""
            
            # 檢查是否需要回溯
            if feedback and loop_count > 1:
                console.print(f"[yellow]📝 Leader 評估: {feedback[:100]}...[/yellow]")
            
            console.print(f"[green]✅ 規劃完成: {' → '.join(order)}[/green]\n")
            
            # 執行規劃
            all_completed = True
            
            for i, agent in enumerate(order):
                console.print(f"\n[yellow]▶ 第 {i+1}/{len(order)}: {agent}[/yellow]")
                
                agent_task = tasks_map.get(agent, f"幫忙完成: {task}")
                
                execute_prompt = f"""你是 {agent}。請根據以下任務執行：

最終任務: {task}
你的專屬任務: {agent_task}

{'之前執行的結果不夠好，請改进。' if feedback else '請執行你的部分工作。'}"""

                result = llm.chat([
                    {"role": "system", "content": f"你是一個專業的 {agent}。"},
                    {"role": "user", "content": execute_prompt}
                ])
                
                if result:
                    console.print(f"[green]✅ {agent} 完成[/green]")
                    console.print(f"[dim]{result[:100]}...[/dim]")
                    
                    # 記錄歷史
                    execution_history.append({
                        "agent": agent,
                        "task": agent_task,
                        "result": result
                    })
                    
                    # 更新 Agent 狀態
                    for a in state.get("agents", []):
                        if a.get("name") == agent:
                            a["status"] = "completed"
                            a["result"] = result
                else:
                    console.print(f"[red]❌ {agent} 失敗[/red]")
                    all_completed = False
            
            config.save_state(team, state)
            
            # 詢問是否繼續或結束
            if loop_count < max_loops:
                # Leader 評估是否繼續
                eval_prompt = f"""之前的執行: {execution_history[-1]['result'][:200]}

任務: {task}

評估結果是否足夠好？回复 "ok" 表示完成，或提出需要改進的地方。"""
                
                eval_result = llm.chat([
                    {"role": "system", "content": "你是 Leader，評估任務完成度。"},
                    {"role": "user", "content": eval_prompt}
                ])
                
                if "ok" in eval_result.lower() and len(eval_result) < 50:
                    console.print(f"\n[green]✅ 全部完成！共 {len(execution_history)} 個步驟[/green]")
                    break
                else:
                    console.print(f"[yellow]📝 繼續改進: {eval_result[:100]}...[/yellow]")
            else:
                console.print(f"\n[yellow]⚠️ 達到最大迴圈次數[/yellow]")
        
    except Exception as e:
        console.print(f"[red]❌ 錯誤: {e}[/red]")
