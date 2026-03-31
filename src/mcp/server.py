"""MCP 伺服器"""
import json
import sys
from typing import Any, Optional

class MCPServer:
    def __init__(self):
        self.tools = {}
        self.resources = {}
    
    def register_tool(self, name: str, handler):
        self.tools[name] = handler
    
    def handle_request(self, msg: dict) -> dict:
        method = msg.get("method", "")
        msg_id = msg.get("id")
        
        if method == "tools/list":
            return {"id": msg_id, "result": {"tools": [{"name": t} for t in self.tools.keys()]}}
        
        if method == "tools/call":
            tool = msg.get("params", {}).get("name")
            args = msg.get("params", {}).get("arguments", {})
            if tool in self.tools:
                result = self.tools[tool](**args) if args else self.tools[tool]()
                return {"id": msg_id, "result": result}
            return {"id": msg_id, "error": {"code": -32601, "message": f"Tool not found: {tool}"}}
        
        return {"id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
    
    def run_stdin(self):
        for line in sys.stdin:
            try:
                msg = json.loads(line)
                response = self.handle_request(msg)
                print(json.dumps(response), flush=True)
            except:
                pass
