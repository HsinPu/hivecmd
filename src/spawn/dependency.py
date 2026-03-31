"""任務依賴管理 - 自動解除封鎖"""
from typing import Optional
from dataclasses import dataclass, field
from rich.console import Console

console = Console()

@dataclass
class Task:
    """任務"""
    id: str
    description: str
    status: str = "pending"  # pending, in_progress, completed, blocked
    owner: Optional[str] = None
    blocked_by: list = field(default_factory=list)
    unblocks: list = field(default_factory=list)  # 這個任務完成後會解除哪些任務
    
class DependencyManager:
    """任務依賴管理器"""
    
    def __init__(self):
        self.tasks: dict[str, Task] = {}
    
    def add_task(self, task: Task):
        """添加任務"""
        self.tasks[task.id] = task
        
        # 建立依賴關係
        for blocked_id in task.blocked_by:
            if blocked_id in self.tasks:
                self.tasks[blocked_id].unblocks.append(task.id)
    
    def update_status(self, task_id: str, status: str):
        """更新任務狀態"""
        if task_id not in self.tasks:
            return
        
        old_status = self.tasks[task_id].status
        self.tasks[task_id].status = status
        
        # 如果任務完成，檢查是否有被阻塞的任務可以解除
        if status == "completed":
            self._unblock_tasks(task_id)
        
        console.print(f"[cyan]{task_id}[/cyan]: {old_status} → {status}")
    
    def _unblock_tasks(self, completed_task_id: str):
        """解除依賴此任務的任務"""
        completed = self.tasks[completed_task_id]
        
        for blocked_id in completed.unblocks:
            blocked = self.tasks[blocked_id]
            
            # 檢查所有依賴是否都滿足
            all_done = all(
                self.tasks.get(bid, Task("","")).status == "completed"
                for bid in blocked.blocked_by
            )
            
            if all_done and blocked.status == "blocked":
                blocked.status = "pending"
                console.print(f"[green]✅ 任務 {blocked_id} 已解除封鎖[/green]")
    
    def get_blocked_tasks(self) -> list[Task]:
        """取得被阻塞的任務"""
        return [t for t in self.tasks.values() if t.status == "blocked"]
    
    def auto_claim(self, agent: str):
        """自動認領可執行的任務"""
        for task in self.tasks.values():
            if task.status == "pending" and task.owner is None:
                task.status = "in_progress"
                task.owner = agent
                console.print(f"[green]🤖 Agent {agent} 認領任務 {task.id}[/green]")
                return task.id
        return None
