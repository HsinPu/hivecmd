# HiveCmd 🤖

Agent Swarm Intelligence CLI - One Command → Full Automation

## 安裝

```bash
pip install hivecmd
# 或從源碼
git clone https://github.com/HsinPu/hivecmd.git
cd hivecmd
pip install -e .
```

## 快速開始

```bash
# 初始化
hivecmd init

# 建立團隊
hivecmd team create my-team --description "我的團隊"

# 生成 Worker Agent
hivecmd spawn agent my-team --name worker1 --task "implement auth"

# 建立任務
hivecmd spawn task my-team --task "implement login"

# 監控團隊
hivecmd board show my-team

# 發送訊息
hivecmd inbox send my-team worker1 "任務完成了吗？"
```

## 命令

| 命令 | 說明 |
|------|------|
| `team create/list/delete/show` | 團隊管理 |
| `spawn agent/task` | 生成 Agent/任務 |
| `board show/attach/serve` | 監控面板 |
| `task list/update/claim` | 任務管理 |
| `inbox send/receive/list` | 訊息收發 |

## 功能

- 🚀 多 Agent 組隊協作
- 📋 智慧任務分配 + 依賴管理
- 💬 Agent 間訊息協調
- 📊 即時監控面板
- 🔄 動態資源調整
- 📦 團隊模板 (對沖基金、Web 開發)

## 技術

- Python 3.10+
- Typer + Rich
- 參考 ClawTeam 重構

## License

MIT
