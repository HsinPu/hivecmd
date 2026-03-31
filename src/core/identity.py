"""Identity - Agent 身份管理"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentIdentity:
    """Agent 身份"""
    name: str
    team: str
    role: str = "worker"
    status: str = "idle"
    task: Optional[str] = None
    inbox: list = None
    
    def __post_init__(self):
        if self.inbox is None:
            self.inbox = []
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "team": self.team,
            "role": self.role,
            "status": self.status,
            "task": self.task,
            "inbox": self.inbox
        }
