# HiveCmd 🤖

AI Agent Swarm Intelligence CLI - One Command → Full Automation

## 功能

14 個 CLI 命令，支援 AI 多 Agent 協作：

### 基本
- `init` - 初始化專案
- `status` - 查看狀態
- `team create/list/show` - 團隊管理

### 生成 & 執行
- `spawn agent` - 生成 Agent (可選 --llm 使用 LLM 執行)
- `spawn task` - 建立任務

### 監控 & 協調
- `board show/serve` - 監控面板
- `task list/update` - 任務管理
- `inbox send/receive` - Agent 間訊息

### 自動化
- `agent create` - AI 自動建立團隊 (使用 LLM)
- `templates create` - 從模板建立團隊
- `mcp tools` - MCP 伺服器
- `gource run` - 可視化
- `lifecycle` - Agent 生命週期

## 安裝

```bash
pip install hivecmd
# 或從源碼
git clone https://github.com/HsinPu/hivecmd.git
cd hivecmd
pip install -e .
```

## 快速開始

### 方式 1：手動建立

```bash
# 建立團隊
hivecmd team create my-team

# 生成 Agent 並執行任務
hivecmd spawn agent my-team -n writer -t "寫一個關於勇氣的故事" --llm
```

### 方式 2：使用模板

```bash
# 從模板建立團隊
hivecmd templates create webapp my-webapp
hivecmd templates create research my-research
hivecmd templates create hedge-fund my-fund
```

### 方式 3：AI 自動建立

```bash
# 設定 API Key
export HIVECMD_LLM_API_KEY=your-key

# AI 分析需求並建立團隊
hivecmd agent create "帮我建立一个做机器学习的团队"
```

## LLM 執行

```bash
# 設定 API Key (OpenRouter)
export HIVECMD_LLM_API_KEY=sk-or-v1-xxx
export HIVECMD_LLM_MODEL=openai/gpt-4o-mini

# 生成 Agent 並讓 LLM 執行任務
hivecmd spawn agent my-team -n worker1 -t "寫一個短篇故事" --llm
```

## 環境變數

```bash
HIVECMD_LLM_API_KEY=your-api-key
HIVECMD_LLM_MODEL=openai/gpt-4o-mini
HIVECMD_LLM_BASE_URL=https://openrouter.ai/api/v1
```

## 功能特色

- 🚀 多 Agent 組隊協作
- 🤖 內建 LLM 執行 (--llm)
- 📋 智慧任務分配 + 依賴管理
- 💬 Agent 間訊息協調
- 📊 Web UI 監控面板
- 📦 團隊模板 (webapp, research, hedge-fund)
- 🔄 Git Worktree 隔離
- 📱 Tmux 會話管理

## 與 ClawTeam 比較

| 項目 | ClawTeam | HiveCmd |
|------|----------|---------|
| 功能覆蓋 | 100% | 100% |
| 程式碼精簡 | 9,070 KB | ~50 KB |
| 內建 LLM | ❌ | ✅ (--llm) |
| Stars | 4,174 | 🆕 |

## 技術

- Python 3.10+
- Typer + Rich
- OpenRouter API

## License

MIT
