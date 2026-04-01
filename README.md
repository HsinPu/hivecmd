# HiveCmd 🤖

AI Agent Swarm Intelligence CLI - One Command → Full Automation

## 功能

14 個 CLI 命令，支援 AI 多 Agent 協作：

### 團隊管理
- `team create/list/show` - 團隊管理
- `templates create` - 從模板建立團隊
- `agent create` - AI 分析需求自動建立團隊 ⭐

### 生成 & 執行
- `spawn agent` - 生成 Agent (可選 --llm 使用 LLM 執行)
- `spawn task` - 建立任務
- `leader run` - **自動協調團隊** ⭐⭐⭐

### 監控 & 協調
- `board show/serve` - 監控面板
- `task list/update` - 任務管理
- `inbox send/receive` - Agent 間訊息

### 其他
- `preset` - 預設配置
- `mcp` - MCP 伺服器
- `gource run` - 可視化
- `lifecycle` - Agent 生命週期
- `init` - 初始化
- `status` - 狀態查看

## 安裝

```bash
pip install hivecmd
# 或從源碼
git clone https://github.com/HsinPu/hivecmd.git
cd hivecmd
pip install -e .
```

## 快速開始

### 1. 建立團隊 (AI 自動分析)

```bash
hivecmd agent create "建立一个写小说的团队"
```

自動產生：
- 團隊描述 (description/about.md)
- 擅長任務 (skills)
- 每個 Agent 的 prompt.md

### 2. 執行任務 (自動選擇團隊)

```bash
# 不指定團隊 → 自動選擇最適合的
hivecmd leader run --task "用繁體中文寫一篇關於環保的文章"

# 指定團隊
hivecmd leader run --team 文章創作團隊 -t "寫一篇關於AI的文章"
```

## Leader 功能 ⭐⭐⭐

Leader 會自動：

1. **讀取 description** - 根據團隊的擅長任務選擇最適合的團隊
2. **規劃執行順序** - 決定誰先誰後
3. **串聯執行** - 每個 Agent 的輸出傳給下一個
4. **即時評估** - 每個執行完立即判斷好壞
5. **自動重做** - 不好的結果會重新執行

```bash
hivecmd leader run --task "寫一篇關於電競滑鼠推薦的文章"
```

### 團隊目錄結構

```
團隊名稱/
├── description/
│   └── about.md        ← 團隊描述 + 擅長任務
├── agents/
│   └── <agent名>/
│       ├── prompt.md   ← Agent 的 system prompt
│       └── output.md   ← 生成的輸出
├── tasks/
└── inbox/
```

## LLM 執行

```bash
# 設定 API Key (OpenRouter)
export HIVECMD_LLM_API_KEY=sk-or-v1-xxx

# 執行任務
hivecmd leader run --task "任務"
```

## 環境變數

```bash
HIVECMD_LLM_API_KEY=your-api-key
HIVECMD_LLM_MODEL=openai/gpt-4o-mini
HIVECMD_LLM_BASE_URL=https://openrouter.ai/api/v1
```

## Skills

HiveCmd 使用 agent-creator-design 規範：

- `src/skills/agent-creator-design/` - System Prompt 設計規範
- `src/system-prompts/` - System Prompt 模板

## 技術

- Python 3.10+
- Typer + Rich
- OpenRouter API

## License

MIT
