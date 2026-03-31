"""Identity - Agent 身份管理 (含類型註解)"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class AgentIdentity:
    """Agent 身份"""
    name: str
    team: str
    role: str = "worker"
    status: str = "idle"
    task: Optional[str] = None
    inbox: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "team": self.team,
            "role": self.role,
            "status": self.status,
            "task": self.task,
            "inbox": self.inbox
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentIdentity":
        return cls(
            name=data.get("name", ""),
            team=data.get("team", ""),
            role=data.get("role", "worker"),
            status=data.get("status", "idle"),
            task=data.get("task"),
            inbox=data.get("inbox", [])
        )
