"""數據收集器"""
from typing import Dict, List
from datetime import datetime

class Collector:
    """數據收集器"""
    
    def __init__(self):
        self.metrics: Dict[str, List] = {
            "tasks_completed": [],
            "tasks_created": [],
            "agents_spawned": [],
            "messages_sent": []
        }
    
    def record(self, metric: str, data: dict):
        """記錄指標"""
        if metric in self.metrics:
            self.metrics[metric].append({
                **data,
                "timestamp": datetime.now().isoformat()
            })
    
    def get_stats(self) -> dict:
        """取得統計"""
        return {
            "total_tasks": len(self.metrics["tasks_completed"]),
            "total_agents": len(self.metrics["agents_spawned"]),
            "total_messages": len(self.metrics["messages_sent"])
        }
    
    def export_csv(self) -> str:
        """匯出 CSV"""
        lines = ["metric,timestamp"]
        for metric, values in self.metrics.items():
            for v in values:
                lines.append(f'{metric},{v.get("timestamp")}')
        return "\n".join(lines)
