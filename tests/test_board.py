"""Board 測試"""
import pytest
from src.board.collector import Collector
from src.board.renderer import Renderer

def test_collector_record():
    """測試記錄指標"""
    c = Collector()
    c.record("tasks_completed", {"task": "test"})
    assert len(c.metrics["tasks_completed"]) == 1

def test_collector_stats():
    """測試統計"""
    c = Collector()
    c.record("tasks_completed", {"task": "test"})
    stats = c.get_stats()
    assert stats["total_tasks"] == 1

def test_render_table():
    """測試表格渲染"""
    r = Renderer()
    table = r.render_table(["Name", "Status"], [["test", "ok"]])
    assert "Name" in table
    assert "Status" in table

def test_render_progress():
    """測試進度條"""
    r = Renderer()
    progress = r.render_progress(3, 10)
    assert "3/10" in progress
