"""團隊模板"""
from typing import Optional
from pathlib import Path

TEAM_TEMPLATES = {
    "hedge-fund": {
        "name": "hedge-fund",
        "description": "投資分析團隊",
        "agents": [
            {"name": "portfolio-manager", "role": "leader", "task": "統籌決策"},
            {"name": "buffett-analyst", "role": "analyst", "task": "價值投資分析"},
            {"name": "growth-analyst", "role": "analyst", "task": "成長投資分析"},
            {"name": "technical-analyst", "role": "analyst", "task": "技術分析"},
            {"name": "risk-manager", "role": "risk", "task": "風險管理"}
        ]
    },
    "webapp": {
        "name": "webapp",
        "description": "全棧 Web 開發團隊",
        "agents": [
            {"name": "architect", "role": "leader", "task": "系統架構"},
            {"name": "backend", "role": "developer", "task": "後端開發"},
            {"name": "frontend", "role": "developer", "task": "前端開發"},
            {"name": "tester", "role": "qa", "task": "測試"}
        ]
    },
    "research": {
        "name": "research",
        "description": "研究團隊",
        "agents": [
            {"name": "lead-researcher", "role": "leader", "task": "研究方向"},
            {"name": "gpu0", "role": "researcher", "task": "實驗 1"},
            {"name": "gpu1", "role": "researcher", "task": "實驗 2"},
            {"name": "gpu2", "role": "researcher", "task": "實驗 3"}
        ]
    }
}

class TemplateManager:
    """模板管理器"""
    
    def __init__(self, custom_dir: Optional[Path] = None):
        self.custom_dir = custom_dir
    
    def list_templates(self) -> list:
        """列出模板"""
        return list(TEAM_TEMPLATES.keys())
    
    def get_template(self, name: str) -> Optional[dict]:
        """取得模板"""
        return TEAM_TEMPLATES.get(name)
    
    def add_template(self, name: str, template: dict):
        """新增模板"""
        TEAM_TEMPLATES[name] = template
    
    def load_from_file(self, path: Path) -> dict:
        """從 TOML 載入"""
        try:
            import toml
            return toml.load(path)
        except:
            return {}
