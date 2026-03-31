"""檔案操作工具"""
import os
import shutil
from pathlib import Path
from typing import Optional

def ensure_dir(path: Path) -> Path:
    """確保目錄存在"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def copy_file(src: Path, dst: Path) -> bool:
    """複製檔案"""
    try:
        shutil.copy2(src, dst)
        return True
    except Exception:
        return False

def read_file(path: Path, encoding: str = "utf-8") -> Optional[str]:
    """讀取檔案"""
    try:
        return path.read_text(encoding=encoding)
    except Exception:
        return None

def write_file(path: Path, content: str, encoding: str = "utf-8") -> bool:
    """寫入檔案"""
    try:
        path.write_text(content, encoding=encoding)
        return True
    except Exception:
        return False

def delete_file(path: Path) -> bool:
    """刪除檔案"""
    try:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
        return True
    except Exception:
        return False
