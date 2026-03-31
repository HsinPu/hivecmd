"""渲染器"""
from typing import Dict, Any

class Renderer:
    """渲染器"""
    
    def __init__(self):
        self.theme = "dark"
    
    def render_table(self, headers: list, rows: list) -> str:
        """渲染表格"""
        lines = []
        # Header
        lines.append(" | ".join(headers))
        lines.append("-" * (len(" | ".join(headers))))
        # Rows
        for row in rows:
            lines.append(" | ".join(str(v) for v in row))
        return "\n".join(lines)
    
    def render_json(self, data: Any) -> str:
        """渲染 JSON"""
        import json
        return json.dumps(data, indent=2)
    
    def render_progress(self, current: int, total: int) -> str:
        """渲染進度條"""
        bar = "█" * current
        empty = "░" * (total - current)
        return f"[{bar}{empty}] {current}/{total}"
