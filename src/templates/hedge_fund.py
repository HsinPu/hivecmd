"""對沖基金模板"""
HEDGE_FUND_TEMPLATE = {
    "name": "hedge-fund",
    "description": "投資分析團隊",
    "agents": [
        {"name": "portfolio-manager", "role": "leader", "task": "統籌決策"},
        {"name": "buffett-analyst", "role": "analyst", "task": "價值投資分析"},
        {"name": "growth-analyst", "role": "analyst", "task": "成長投資分析"},
        {"name": "technical-analyst", "role": "analyst", "task": "技術分析"},
        {"name": "risk-manager", "role": "risk", "task": "風險管理"},
    ]
}
