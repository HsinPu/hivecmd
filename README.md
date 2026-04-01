# HiveCmd 🤖

AI Agent Swarm Intelligence CLI - One Command → Full Automation

## 功能

14 個 CLI 命令，支援 AI 多 Agent 協作：

### 團隊管理
- `team create/list/show` - 團隊管理
- `templates create` - 從模板建立團隊
- `agent create` - AI 分析需求自動建立團隊

### 生成 & 執行
- `spawn agent` - 生成 Agent (可選 --llm 使用 LLM 執行)
- `spawn task` - 建立任務
- `leader run` - **Leader 自動協調團隊** ⭐

### 監控 & 協調
- `board show/serve` - 監控面板
- `task list/update` - 任務管理
- `inbox send/receive` - Agent 間訊息

### 其他
- `preset` - 預設配置
- `mcp` - MCP 伺服器
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

### 1. 建立團隊 (三種方式)

```bash
# 方式 1: 手動建立
hivecmd team create my-team

# 方式 2: 從模板建立
hivecmd templates create webapp my-team
hivecmd templates create research my-research

# 方式 3: AI 分析建立
hivecmd agent create "建立一个写小说的团队"
```

### 2. 執行任務

```bash
# 單一 Agent 執行
hivecmd spawn agent my-team -n writer -t "寫一個故事" --llm

# Leader 自動協調 (自動分配給團隊成員) ⭐
hivecmd leader run my-team -t "完成一個小說"
```

## LLM 執行

```bash
# 設定 API Key (OpenRouter)
export HIVECMD_LLM_API_KEY=sk-or-v1-xxx

# 執行任務
hivecmd spawn agent my-team -n worker -t "任務" --llm
```

## Leader 功能 ⭐

Leader 會自動：
1. 分析任務
2. 規劃執行順序
3. 分配給團隊成員執行
4. 監控完成

```bash
hivecmd leader run 小說創作團隊 -t "完成時光之門小說"
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
- 👑 Leader 自動協調 ⭐
- 📋 智慧任務分配
- 💬 Agent 間訊息
- 📊 Web UI 監控
- 📦 團隊模板

## 與 ClawTeam 比較

| 項目 | ClawTeam | HiveCmd |
|------|----------|---------|
| 功能覆蓋 | 100% | 100% |
| 程式碼精簡 | 9,070 KB | ~50 KB |
| 內建 LLM | ❌ | ✅ |
| Leader 協調 | 需要外部 Claude | 內建 ⭐ |
| Stars | 4,174 | 🆕 |

## 技術

- Python 3.10+
- Typer + Rich
- OpenRouter API

## License

MIT
