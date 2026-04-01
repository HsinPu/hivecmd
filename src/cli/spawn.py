"""Spawn 命令 - 生成 Agent (含 LLM 執行)"""
import typer
from rich.console import Console
from ..core.config import Config
from ..core.identity import AgentIdentity
from ..services.llm import LLMService

spawn_app = typer.Typer(name="spawn", help="生成 Worker Agent")
console = Console()

@spawn_app.command("agent", help="生成 Agent")
def spawn_agent(
    team: str = typer.Argument(..., help="團隊名"),
    name: str = typer.Option(None, "--name", "-n", help="Agent 名稱"),
    task: str = typer.Option("", "--task", "-t", help="任務描述"),
    agent_type: str = typer.Option("claude", "--type", help="Agent 類型"),
    use_llm: bool = typer.Option(False, "--llm", help="使用 LLM 執行任務")
):
    """生成 Worker Agent"""
    config = Config()
    state = config.load_state(team)
    
    agent_id = name or f"agent-{len(state.get('agents', [])) + 1}"
    
    # 建立 Agent 身份
    identity = AgentIdentity(
        name=agent_id,
        team=team,
        role="worker",
        status="active",
        task=task
    )
    
    # 保存 Agent
    agents = state.get("agents", [])
    agents.append(identity.to_dict())
    state["agents"] = agents
    config.save_state(team, state)
    
    console.print(f"[green]✅ Agent '{agent_id}' 已生成[/green]")
    console.print(f"[dim]類型: {agent_type} | 任務: {task or '無'}[/dim]")
    
    # 如果啟用 LLM，則執行任務
    if use_llm and task:
        console.print(f"\n[cyan]🤖 Agent '{agent_id}' 正在執行任務...[/cyan]")
        
        llm = LLMService()
        
        if not llm.api_key:
            console.print("[red]❌ 請設定 API Key:[/red]")
            console.print("[dim]export HIVECMD_LLM_API_KEY=your-key[/dim]")
            return
        
        # 構建 prompt
        system_prompt = f"""你是一個專業的 {agent_type} Agent。請根據任務執行工作。

團隊: {team}
Agent: {agent_id}
任務: {task}

請直接執行任務，完成後回報結果。"""

        result = llm.chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task}
        ])
        
        if result:
            console.print(f"\n[green]✅ 任務完成:[/green]")
            console.print(result[:500] + "..." if len(result) > 500 else result)
            
            # 更新 Agent 狀態
            for a in state["agents"]:
                if a["name"] == agent_id:
                    a["status"] = "completed"
                    a["result"] = result
            config.save_state(team, state)
        else:
            console.print("[red]❌ LLM 執行失敗[/red]")
    
    # 建立 Worktree (如果 git repo 存在)
    try:
        from ..spawn.worktree import WorktreeManager
        wm = WorktreeManager()
        wt = wm.create_worktree(team, agent_id)
        if wt:
            console.print(f"[dim]Worktree: {wt}[/dim]")
    except Exception as e:
        pass
    
    # 建立 Tmux 會話
    try:
        from ..spawn.tmux import TmuxManager
        tm = TmuxManager()
        tm.create_session(team, agent_id)
    except:
        pass

@spawn_app.command("task", help="生成任務")
def spawn_task(
    team: str = typer.Argument(..., help="團隊名"),
    description: str = typer.Option(..., "--task", "-t", help="任務描述"),
    blocked_by: str = typer.Option(None, help="依賴任務 ID")
):
    """生成任務"""
    config = Config()
    state = config.load_state(team)
    
    task_id = f"task-{len(state.get('tasks', [])) + 1}"
    
    task = {
        "id": task_id,
        "description": description,
        "status": "pending",
        "blocked_by": blocked_by,
        "owner": None
    }
    
    tasks = state.get("tasks", [])
    tasks.append(task)
    state["tasks"] = tasks
    config.save_state(team, state)
    
    console.print(f"[green]✅ 任務 '{task_id}' 已建立[/green]")
    if blocked_by:
        console.print(f"[dim]依賴: {blocked_by}[/dim]")
