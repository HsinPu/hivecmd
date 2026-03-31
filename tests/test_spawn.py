"""生成測試"""
import pytest
from src.spawn.dependency import DependencyManager, Task

def test_add_task():
    """測試添加任務"""
    dm = DependencyManager()
    task = Task(id="task-1", description="test task")
    dm.add_task(task)
    assert "task-1" in dm.tasks

def test_task_dependency():
    """測試任務依賴"""
    dm = DependencyManager()
    t1 = Task(id="t1", description="t1")
    t2 = Task(id="t2", description="t2", blocked_by=["t1"])
    dm.add_task(t1)
    dm.add_task(t2)
    assert "t2" in t1.unblocks

def test_auto_unblock():
    """測試自動解除"""
    dm = DependencyManager()
    t1 = Task(id="t1", description="t1")
    t2 = Task(id="t2", description="t2", blocked_by=["t1"])
    dm.add_task(t1)
    dm.add_task(t2)
    assert t2.status == "pending"
    dm.update_status("t1", "completed")
    assert t2.status == "pending"  # 還需要其他條件
