"""LLM Service - 使用 OpenRouter API"""
import os
import json
from typing import List, Dict

class LLMService:
    def __init__(self):
        self.api_key = os.environ.get("HIVECMD_LLM_API_KEY")
        self.model = os.environ.get("HIVECMD_LLM_MODEL") or "openai/gpt-4o-mini"
        self.base_url = os.environ.get("HIVECMD_LLM_BASE_URL") or "https://openrouter.ai/api/v1"
    
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
        """AI 分析團隊需求 - 使用 agent-creator-design 規則"""
        system_prompt = """你是團隊規劃師，專精於設計高效的 AI Agent。

請根據用戶需求返回 JSON 格式的團隊配置。

## 設計規則 (agent-creator-design)

每個 Agent 必須遵循以下設計原則：

### 1. 單一職責
- 每個 Agent 只定義一個角色或一類任務
- 避免「什麼都能做」的通用型描述

### 2. 四大項結構
每個 Agent 的設定必須包含：
- **Role (角色)**: 一句話定義「你是誰」
- **Task (任務)**: 要完成的具體工作
- **Constraints (規範)**: 必須遵守的規則
- **Output (輸出)**: 產出形式與格式

### 3. 命名規範
- 使用 lowercase + hyphen (如 story-writer, character-designer)
- 名稱語意清楚，長度適中

## 返回格式

```json
{
  "template": "模板名稱",
  "team_name": "團隊名稱",
  "description": "團隊描述",
  "agents": [
    {
      "name": "agent-name",
      "role": "Agent 角色描述 (一句話)",
      "task": "Agent 的主要任務"
    }
  ]
}
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
