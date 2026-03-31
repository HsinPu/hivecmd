"""Gource 可視化"""
import subprocess
from pathlib import Path

class GourceRenderer:
    def __init__(self, repo: Path):
        self.repo = repo
        self.log_file = repo / ".gource.log"
    
    def generate_log(self, events: list):
        lines = []
        import time
        ts = int(time.time())
        for e in events:
            action = e.get("action", "A")
            path = e.get("path", "/")
            user = e.get("user", "hivecmd")
            lines.append(f"{ts} | {action} | {path} | {user}")
        self.log_file.write_text("\n".join(lines))
        return self.log_file
    
    def run(self):
        try:
            subprocess.run(["gource", str(self.log_file)], cwd=self.repo)
            return True
        except:
            return False
