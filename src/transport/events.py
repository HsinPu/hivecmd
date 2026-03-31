"""事件系統"""
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Any

@dataclass
class Event:
    type: str
    source: str
    target: str
    data: Any
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class EventBus:
    """事件匯流排"""
    
    def __init__(self):
        self.listeners: dict[str, list[Callable]] = {}
    
    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
    
    def publish(self, event: Event):
        for callback in self.listeners.get(event.type, []):
            callback(event)
