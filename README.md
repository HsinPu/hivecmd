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
# 建立團隊
hivecmd team create my-team

# 生成 Worker Agent
hivecmd spawn --team my-team --agent worker1 --task "implement auth"

# 監控
hivecmd board attach my-team
```

## 功能

- 🚀 多 Agent 組隊協作
- 📋 智慧任務分配
- 💬 子 Agent 協調
- 📊 即時監控面板
- 🔄 動態資源調整
