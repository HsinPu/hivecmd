"""Agent 調度 - 調用外部 AI Agent"""
import subprocess
import os
from dataclasses import dataclass
from typing import Optional
from rich.console import Console

console = Console()

@dataclass
class AgentConfig:
    """Agent 配置"""
    name: str
    cli: str  # claude, codex, openclaw 等
    model: Optional[str] = None
    api_key: Optional[str] = None

class AgentScheduler:
    """Agent 調度器"""
    
    SUPPORTED_AGENTS = {
        "claude": ["claude", "claude-code"],
        "codex": ["codex"],
        "openclaw": ["openclaw"],
        "nanobot": ["nanobot"],
    }
    
    def __init__(self):
        self.running_agents = {}
    
    def check_agent_available(self, cli: str) -> bool:
        """檢查 Agent CLI 是否可用"""
        result = subprocess.run(
            ["which", cli],
            capture_output=True
        )
        return result.returncode == 0
    
    def spawn_agent(
        self,
        team: str,
        agent_name: str,
        task: str,
        cli: str = "claude",
        model: str = None
    ) -> bool:
        """生成 Agent 並執行任務"""
        if not self.check_agent_available(cli):
            console.print(f"[red]❌ {cli} 不可用，請先安裝[/red]")
            return False
        
        # 構建命令
        cmd = self._build_command(cli, task, model)
        
        console.print(f"[cyan]🤖 啟動 {cli} Agent: {agent_name}[/cyan]")
        console.print(f"[dim]任務: {task}[/dim]")
        
        # 這裡只是記錄，不實際執行長時間的 Agent
        self.running_agents[f"{team}/{agent_name}"] = {
            "cli": cli,
            "task": task,
            "status": "spawned"
        }
        
        return True
    
    def _build_command(self, cli: str, task: str, model: str = None) -> list:
        """構建命令"""
        if cli in ["claude", "claude-code"]:
            cmd = [cli, "--print"]
            if model:
                cmd.extend(["--model", model])
        elif cli == "codex":
            cmd = [cli, "complete", task]
        else:
            cmd = [cli, "exec", task]
        
        return cmd
    
    def kill_agent(self, team: str, agent_name: str):
        """結束 Agent"""
        key = f"{team}/{agent_name}"
        if key in self.running_agents:
            del self.running_agents[key]
            console.print(f"[red]🛑 Agent {agent_name} 已結束[/red]")
    
    def list_agents(self, team: str = None) -> list:
        """列出運行的 Agents"""
        result = []
        for key, info in self.running_agents.items():
            if team and not key.startswith(team):
                continue
            result.append({"key": key, **info})
        return result
