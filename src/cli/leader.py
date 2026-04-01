"""Leader 命令 - 自動協調 (串联执行)"""
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
    """Leader 會分析任務並分配給團隊成員執行，輸出會串聯傳遞"""
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
        all_outputs = {}  # 收集所有輸出
        
        while loop_count < max_loops:
            loop_count += 1
            console.print(f"\n[cyan]=== 迴圈 {loop_count}/{max_loops} ===[/cyan]")
            
            # Leader 規劃
            console.print("[yellow]🤔 Leader 分析任務...[/yellow]")
            
            # 加入之前的輸出作為 context
            context = ""
            if all_outputs:
                context = "\n之前的結果:\n"
                for name, output in all_outputs.items():
                    context += f"- {name}: {output[:150]}...\n"
            
            plan_prompt = f"""你是一個團隊 Leader。你需要分析任務並決定執行順序。

團隊成員: {', '.join(agent_names)}
最終任務: {task}
{context}

每個成員的輸出會傳給下一個，所以請安排順序讓他們能接續工作。
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
            
            # ===== 串联执行 =====
            previous_output = ""  # 前一個 Agent 的輸出
            
            for i, agent in enumerate(order):
                execution_count += 1
                console.print(f"\n[yellow]▶ [{execution_count}] {agent}[/yellow]")
                
                agent_task = tasks_map.get(agent, f"幫忙完成: {task}")
                
                # 构建提示 - 加入之前的输出
                if previous_output:
                    execute_prompt = f"""你是 {agent}。請根據以下任務執行：

最終任務: {task}
你的專屬任務: {agent_task}

前面成員的結果（供你參考）:
{previous_output}

請執行你的部分，並將結果傳給下一個成員。"""
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
                    console.print(f"[green]✅ {agent} 完成[/green]")
                    console.print(f"[dim]{result[:80]}...[/dim]")
                    
                    # 保存输出 - 用于串联
                    all_outputs[agent] = result
                    
                    # 更新为下一个准备
                    previous_output = result
                    
                    # 即时评估
                    eval_prompt = f"""評估：

任務: {task}
{agent} 的結果: {result}

回复 "ok" 如果完成，或简短说明需要改进。"""

                    eval_result = llm.chat([
                        {"role": "system", "content": "评估结果。"},
                        {"role": "user", "content": eval_prompt}
                    ])
                    
                    if "ok" not in eval_result.lower() or len(eval_result) > 30:
                        console.print(f"[yellow]⚠️ 需改進: {eval_result[:80]}...[/yellow]")
                        # 重新执行
                        retry_prompt = f"""你是 {agent}。之前結果不夠好：
{eval_result}

請重新執行，任務: {agent_task}
之前輸出: {previous_output}

改進上述问题。"""

                        retry_result = llm.chat([
                            {"role": "system", "content": f"你是專業的 {agent}。"},
                            {"role": "user", "content": retry_prompt}
                        ])
                        
                        if retry_result:
                            console.print(f"[green]✅ {agent} 重新完成[/green]")
                            all_outputs[agent] = retry_result
                            previous_output = retry_result
                    
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
                    {"role": "user", "content": f"任务: {task}. 共 {len(all_outputs)} 個成員完成。回复 'ok' 如果完成。"}
                ])
                
                if "ok" in final_eval.lower() and len(final_eval) < 30:
                    console.print(f"\n[green]✅ 全部完成！共 {execution_count} 次執行[/green]")
                    break
        
        console.print(f"\n[yellow]⚠️ 完成 ({execution_count} 次執行)[/yellow]")
        
    except Exception as e:
        console.print(f"[red]❌ 錯誤: {e}[/red]")
