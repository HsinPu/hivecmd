"""LLM Service - 使用 OpenRouter API"""
import os
import json
from typing import List, Dict

class LLMService:
    def __init__(self):
        self.api_key = os.environ.get("HIVECMD_LLM_API_KEY")
        self.model = os.environ.get("HIVECMD_LLM_MODEL") or "openai/gpt-4o-mini"
        self.base_url = os.environ.get("HIVECMD_LLM_BASE_URL") or "https://openrouter.ai/api/v1"
        self.skills_dir = os.path.join(os.path.dirname(__file__), "..", "skills")
    
    def get_skill(self, skill_name: str) -> str:
        """讀取 SKILL.md 檔案"""
        skill_path = os.path.join(self.skills_dir, skill_name, "SKILL.md")
        if os.path.exists(skill_path):
            with open(skill_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""
    
    def chat(self, messages: List[Dict]) -> str:
        """發送聊天請求"""
        if not self.api_key:
            return ""
        
        try:
            import requests
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": messages
            }
            response = requests.post(f"{self.base_url}/chat/completions", 
                                   headers=headers, json=data, timeout=120)
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error: {e}")
        return ""
    
    def analyze_team_need(self, user_request: str) -> Dict:
        """AI 分析團隊需求 - 動態讀取 SKILL.md"""
        # 讀取 agent-creator-design skill
        skill_content = self.get_skill("agent-creator-design")
        
        system_prompt = f"""你是團隊規劃師，專精於設計高效的 AI Agent。

## 設計規則 (來自 SKILL.md)

{skill_content}

## 你的任務

根據用戶需求，返回 JSON 格式的團隊配置。

返回格式：
```json
{{
  "template": "模板名稱",
  "team_name": "團隊名稱", 
  "description": "團隊描述",
  "agents": [
    {{
      "name": "agent-name",
      "role": "Agent 角色 (一句話)",
      "task": "Agent 的主要任務"
    }}
  ]
}}
```

只返回 JSON，不要其他文字。"""

        result = self.chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_request}
        ])
        
        if result:
            import re
            m = re.search(r'\{[\s\S]*\}', result)
            if m:
                try:
                    return json.loads(m.group())
                except:
                    pass
        
        return {
            "template": "custom",
            "team_name": "ai-team",
            "description": "AI 團隊",
            "agents": [
                {"name": "worker", "role": "工作者", "task": "執行任務"}
            ]
        }
