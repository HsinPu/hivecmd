"""Agent 生命週期管理"""
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional

@dataclass
class LifecycleEvent:
    event: str
    team: str
    agent: str
    timestamp: datetime

class LifecycleManager:
    """生命週期管理器"""
    
    def __init__(self):
        self.hooks: dict[str, list[Callable]] = {
            "on_spawn": [],
            "on_idle": [],
            "on_working": [],
            "on_complete": [],
            "on_error": [],
            "on_stop": []
        }
    
    def register(self, event: str, callback: Callable):
        """註冊鉤子"""
        if event in self.hooks:
            self.hooks[event].append(callback)
    
    def trigger(self, event: str, team: str, agent: str):
        """觸發事件"""
        e = LifecycleEvent(event, team, agent, datetime.now())
        for callback in self.hooks.get(event, []):
            try:
                callback(e)
            except Exception:
                pass
    
    def on_spawn(self, callback: Callable):
        self.register("on_spawn", callback)
    
    def on_complete(self, callback: Callable):
        self.register("on_complete", callback)
