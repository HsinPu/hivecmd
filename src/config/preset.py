"""預設配置管理"""
from typing import Optional

PRESETS = {
    "moonshot-cn": {
        "provider": "moonshot",
        "base_url": "https://api.moonshot.cn/v1",
        "model": "moonshot-v1-8k"
    },
    "openai": {
        "provider": "openai",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o"
    },
    "anthropic": {
        "provider": "anthropic", 
        "base_url": "https://api.anthropic.com",
        "model": "claude-sonnet-4-20250514"
    },
    "azure": {
        "provider": "azure",
        "base_url": "https://your-resource.openai.azure.com",
        "model": "gpt-4"
    }
}

class PresetManager:
    """預設配置管理器"""
    
    def __init__(self):
        self.current = "openai"
    
    def list_presets(self) -> list:
        """列出所有預設"""
        return list(PRESETS.keys())
    
    def get_preset(self, name: str) -> Optional[dict]:
        """取得預設"""
        return PRESETS.get(name)
    
    def use_preset(self, name: str) -> bool:
        """使用預設"""
        if name in PRESETS:
            self.current = name
            return True
        return False
    
    def add_preset(self, name: str, config: dict):
        """新增預設"""
        PRESETS[name] = config
