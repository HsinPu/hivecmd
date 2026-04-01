"""Leader 命令 - 自動協調"""
import os
import typer
import re
import json
from pathlib import Path
from rich.console import Console
from ..core.config import Config
from ..services.llm import LLMService

leader_app = typer.Typer(name="leader", help="Leader 自動協調")
console = Console()

def get_prompt(name: str, prompt_type: str = "leader") -> str:
    """讀取 prompt.md"""
    if prompt_type == "leader":
        path = Path(__file__).parent.parent / "system-prompts" / name / "prompt.md"
    else:
        path = Path(__file__).parent.parent.parent / ".hivecmd" / "teams" / name / "agents" / prompt_type / "prompt.md"
    
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def get_team_description(team_name: str) -> str:
    """讀取團隊的 description/about.md"""
    path = Path.home() / ".hivecmd" / "teams" / team_name / "description" / "about.md"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def save_output(team_dir: Path, agent_name: str, result: str):
    """儲存 Agent 輸出"""
    agents_dir = team_dir / "agents"
    (agents_dir / agent_name).mkdir(exist_ok=True)
    
    output_file = agents_dir / agent_name / "output.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)
    
    return output_file

def list_teams():
    """列出所有團隊 (讀取 description/about.md)"""
    teams_dir = Path.home() / ".hivecmd" / "teams"
    if not teams_dir.exists():
        return []
    teams = []
    for d in teams_dir.iterdir():
        if d.is_dir():
            # 讀取 description/about.md
            desc_file = d / "description" / "about.md"
            if desc_file.exists():
                try:
                    with open(desc_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        teams.append({
                            "name": d.name,
                            "description": content
                        })
                except:
                    pass
    return teams

def auto_select_team(llm, task: str, teams: list) -> str:
    """讓 LLM 根據 description 選擇最適合的團隊"""
    if not teams:
        return None
    
    teams_info = "\n".join([f"## {t['name']}\n{t['description']}" for t in teams])
    
    prompt = f"""根據以下任務，選擇最適合的團隊：

任務: {task}

可用團隊:
{teams_info}

只返回團隊名稱，不要其他文字。"""

    result = llm.chat([
        {"role": "system", "content": "你是一個團隊選擇專家，擅長根據團隊描述選擇最適合的團隊。"},
        {"role": "user", "content": prompt}
    ])
    
    for t in teams:
        if t["name"] in result:
            return t["name"]
    
    return teams[0]["name"] if teams else None

@leader_app.command("run", help="啟動 Leader 協調")
def leader_run(
    team: str = typer.Option(None, "--team", help="團隊名稱 (可選)"),
    task: str = typer.Option(..., "--task", "-T", help="最終任務")
):
    """Leader 會分析任務並串聯執行每個 Agent，即時評估"""
    try:
        config = Config()
        llm = LLMService()
        
        if not llm.api_key:
            console.print("[red]❌ 請設定 API Key[/red]")
            return
        
        # 如果沒有指定團隊，自動選擇 (根據 description/about.md)
        if not team:
            console.print("[yellow]🔍 自動選擇最適合的團隊...[/yellow]")
            teams = list_teams()
            if not teams:
                console.print("[red]❌ 沒有可用的團隊[/red]")
                return
            
            team = auto_select_team(llm, task, teams)
            console.print(f"[green]✅ 選擇團隊: {team}[/green]")
        
        # 讀取 Leader prompt
        leader_prompt = get_prompt("leader", "leader")
        
        state = config.load_state(team)
        agents = state.get("agents", [])
        
        if not agents:
            console.print(f"[red]❌ 團隊 '{team}' 沒有 Agent[/red]")
            return
        
        agent_names = [a.get("name") for a in agents]
        team_dir = config.get_team_dir(team)
        
        console.print(f"\n[cyan]🤖 啟動 Leader: {team}[/cyan]")
        console.print(f"[dim]任務: {task}[/dim]\n")
        
        # Leader 規劃
        console.print("[yellow]🤔 Leader 分析任務...[/yellow]")
        
        plan_prompt = f"""{leader_prompt}

## 任務資訊

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
        
        match = re.search(r'\{[\s\S]*\}', plan_result)
        if match:
            plan = json.loads(match.group())
            order = plan.get("order", agent_names[:3])
            tasks_map = plan.get("tasks", {})
        else:
            order = agent_names[:3]
            tasks_map = {a: f"幫忙完成: {task}" for a in order}
        
        console.print(f"[green]✅ 規劃: {' → '.join(order)}[/green]\n")
        
        # 串聯執行
        previous_output = ""
        
        for i, agent in enumerate(order):
            console.print(f"\n[yellow]▶ {agent}[/yellow]")
            
            agent_task = tasks_map.get(agent, f"幫忙完成: {task}")
            
            # 讀取 Agent 的 prompt.md → 放到 system prompt
            agent_prompt = get_prompt(team, agent)
            
            if agent_prompt:
                console.print(f"[dim]📖 讀取 prompt: {agent}.md[/dim]")
            
            # User prompt 只放任務相關資訊
            if previous_output:
                user_prompt = f"""## 任務
最終任務: {task}
你的專屬任務: {agent_task}

## 前面的輸出
{previous_output}

請根據你的角色執行任務，並將結果傳給下一個成員。"""
            else:
                user_prompt = f"""## 任務
最終任務: {task}
你的專屬任務: {agent_task}

請執行你的部分。"""

            # System prompt 包含 agent 的 prompt.md
            result = llm.chat([
                {"role": "system", "content": f"{agent_prompt}"},
                {"role": "user", "content": user_prompt}
            ])
            
            if result:
                console.print(f"[green]✅ 完成[/green]")
                console.print(f"[dim]{result[:60]}...[/dim]")
                
                # 儲存輸出
                output_file = save_output(team_dir, agent, result)
                console.print(f"[dim]💾 輸出: {agent}/output.md[/dim]")
                
                # 即時評估
                eval_result = llm.chat([
                    {"role": "system", "content": "即时评估。"},
                    {"role": "user", "content": f"評估: {task}\n{agent} 結果: {result}\n回复 ok 或改進建議"}
                ])
                
                if "ok" not in eval_result.lower() or len(eval_result) > 30:
                    console.print(f"[yellow]⚠️ 需改進: {eval_result[:60]}...[/yellow]")
                    
                    retry_result = llm.chat([
                        {"role": "system", "content": agent_prompt},
                        {"role": "user", "content": f"結果需改進: {eval_result}\n任務: {agent_task}\n請改進"}
                    ])
                    
                    if retry_result:
                        console.print(f"[green]✅ 重新完成[/green]")
                        result = retry_result
                        output_file = save_output(team_dir, agent, result)
                
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
