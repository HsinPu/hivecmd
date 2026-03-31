"""LLM 服務"""
import json
import os
from typing import Dict, List, Optional

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("HIVECMD_LLM_API_KEY", "")
        self.base_url = os.getenv("HIVECMD_LLM_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = os.getenv("HIVECMD_LLM_MODEL", "openai/gpt-4o-mini")
    
    def chat(self, messages: List[Dict[str, str]]) -> Optional[str]:
        if not self.api_key:
            return None
        try:
            import requests
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": self.model, "messages": messages, "temperature": 0.7},
                timeout=30
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
        except:
            pass
        return None
    
    def analyze_team_need(self, user_request: str) -> Dict:
        system_prompt = """你是團隊規劃師。根據用戶請求返回 JSON：

可用模板：webapp, hedge-fund, research

返回格式：
{"template": "模板", "team_name": "名稱", "description": "描述", "agents": [{"name": "名", "role": "角色", "task": "任務"}]}

只返回 JSON。"""

        result = self.chat([{"role": "system", "content": system_prompt}, {"role": "user", "content": user_request}])
        
        if result:
            import re
            m = re.search(r'\{[\s\S]*\}', result)
            if m:
                try:
                    return json.loads(m.group())
                except:
                    pass
        
        return {"template": "webapp", "team_name": "ai-team", "description": "AI團隊", 
                "agents": [{"name": "leader", "role": "leader", "task": "協調"}, {"name": "dev", "role": "developer", "task": "開發"}]}
