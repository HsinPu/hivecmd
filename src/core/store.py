"""持久化儲存"""
import json
from pathlib import Path
from typing import Optional, Any
import time

class Store:
    """Key-Value 儲存"""
    
    def __init__(self, path: Path):
        self.path = path
        self.path.mkdir(parents=True, exist_ok=True)
    
    def get(self, key: str) -> Optional[Any]:
        """取得值"""
        file = self.path / f"{key}.json"
        if file.exists():
            return json.loads(file.read_text())
        return None
    
    def set(self, key: str, value: Any):
        """設定值"""
        file = self.path / f"{key}.json"
        file.write_text(json.dumps(value, indent=2))
    
    def delete(self, key: str):
        """刪除值"""
        file = self.path / f"{key}.json"
        if file.exists():
            file.unlink()
    
    def list(self) -> list:
        """列出所有鍵"""
        return [f.stem for f in self.path.glob("*.json")]
    
    def get_or_set(self, key: str, default: Any) -> Any:
        """取得或設定"""
        val = self.get(key)
        if val is None:
            val = default()
            self.set(key, val)
        return val
