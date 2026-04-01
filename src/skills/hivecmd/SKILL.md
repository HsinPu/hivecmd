# HiveCmd Skills

## 概述

HiveCmd 專屬技能設定

## 技能

### 1. Agent Swarm Coordination

使用 Leader 自動協調多個 Agent：

```bash
hivecmd leader run <團隊> -t <任務>
```

功能：
- 自動分析任務
- 規劃執行順序
- 串聯輸出 (前一個輸出傳給下一個)
- 即時評估 (每個執行完立即判斷好壞)
- 自動重做 (不好的結果會重新執行)

### 2. LLM Task Execution

使用 --llm 讓 Agent 執行 LLM 任務：

```bash
hivecmd spawn agent <團隊> -n <agent名> -t <任務> --llm
```

### 3. Team Templates

從模板建立團隊：

```bash
hivecmd templates create webapp <團隊名>
hivecmd templates create research <團隊名>
```

## 環境變數

```bash
HIVECMD_LLM_API_KEY=your-api-key
HIVECMD_LLM_MODEL=openai/gpt-4o-mini
```

## 範例

```bash
# 建立團隊
hivecmd agent create "建立一個寫小說的團隊"

# Leader 執行
hivecmd leader run 小說團隊 -t "寫一個關於勇氣的故事"

# 查看狀態
hivecmd board show 小說團隊
```
