---
name: hivecmd
description: Agent Swarm Intelligence CLI - use for multi-agent coordination, task delegation, and collaborative AI development. Spawns worker agents with independent git worktrees and tmux sessions. Supports Claude Code, Codex, OpenClaw, and custom agents.
version: 1.0.0
metadata: { "openclaw": { "emoji": "🐝", "requires": { "bins": ["python3", "tmux"], "env": [] }, "primaryEnv": "", "homepage": "https://github.com/HsinPu/hivecmd", "install": [{ "id": "git", "kind": "git", "repo": "https://github.com/HsinPu/hivecmd", "label": "Install HiveCmd" }] } }
---

# HiveCmd - Agent Swarm Intelligence

HiveCmd enables AI agents to work as a coordinated team. The leader agent spawns workers, assigns tasks, and manages coordination through CLI commands.

## When to Use HiveCmd

- **Multi-agent collaboration**: Split complex tasks across multiple agents
- **Autonomous research**: Run parallel experiments on multiple GPUs
- **Full-stack development**: Coordinate frontend, backend, and QA agents
- **Team templates**: Launch pre-built team archetypes (hedge fund, webapp)
- **Real-time monitoring**: Track progress via Web UI or terminal

## Installation

### Via Git Clone
```bash
git clone https://github.com/HsinPu/hivecmd.git
cd hivecmd
pip install -e .
```

### Via pip
```bash
pip install hivecmd
```

## Quick Start

### 1. Create a Team
```bash
hivecmd team create my-team --description "Build authentication"
```

### 2. Spawn Worker Agents
```bash
# Spawn multiple workers
hivecmd spawn agent my-team --name backend --task "Implement JWT auth"
hivecmd spawn agent my-team --name frontend --task "Build React login form"
hivecmd spawn agent my-team --name tester --task "Write auth tests"
```

### 3. Create Tasks with Dependencies
```bash
hivecmd spawn task my-team --task "Design API schema" --blocked-by null
hivecmd spawn task my-team --task "Implement auth" --blocked-by task-1
```

### 4. Monitor Progress
```bash
hivecmd board show my-team
# Or use Web UI
hivecmd board serve --port 8080
```

### 5. Agent Communication
```bash
# Send message to agent
hivecmd inbox send my-team backend "API schema ready"
# Check inbox
hivecmd inbox receive my-team backend
```

## Common Workflows

### Workflow 1: Multi-Agent Development

1. **Create team and spawn agents**:
   ```bash
   hivecmd team create webapp
   hivecmd spawn agent webapp --name architect --task "Design system"
   hivecmd spawn agent webapp --name backend --task "Build API"
   hivecmd spawn agent webapp --name frontend --task "Build UI"
   ```

2. **Create tasks with dependencies**:
   ```bash
   hivecmd spawn task webapp --task "Design REST API" --blocked-by null
   hivecmd spawn task webapp --task "Implement endpoints" --blocked-by task-1
   hivecmd spawn task webapp --task "Build React components" --blocked-by task-1
   ```

3. **Monitor and coordinate**:
   ```bash
   hivecmd board show webapp
   hivecmd inbox send webapp backend "Schema complete"
   ```

### Workflow 2: Autonomous Research

1. **Create research team**:
   ```bash
   hivecmd team create research --description "ML experiments"
   ```

2. **Spawn research agents**:
   ```bash
   hivecmd spawn agent research --name gpu0 --task "Explore depth 10-16"
   hivecmd spawn agent research --name gpu1 --task "Explore width 80-128"
   hivecmd spawn agent research --name gpu2 --task "Tune learning rate"
   ```

3. **Check results**:
   ```bash
   hivecmd board show research
   ```

### Workflow 3: Use Web UI

```bash
hivecmd board serve --port 8080
# Open http://localhost:8080
```

## Command Reference

| Command | Purpose |
|---------|---------|
| `team create <name>` | Create a new team |
| `team list` | List all teams |
| `team show <name>` | Show team details |
| `team delete <name>` | Delete a team |
| `spawn agent <team> --name <name> --task <task>` | Spawn a worker agent |
| `spawn task <team> --task <desc> --blocked-by <id>` | Create a task |
| `board show <team>` | Show team status |
| `board attach <team>` | Attach to tmux session |
| `board serve --port <port>` | Start Web UI |
| `task list <team>` | List tasks |
| `task update <team> <id> --status <status>` | Update task |
| `task claim <team> <id> <agent>` | Claim task |
| `inbox send <team> <to> <message>` | Send message |
| `inbox receive <team> <agent>` | Receive messages |
| `status [team]` | Show status |

## Agent Types

HiveCmd supports multiple AI agent CLIs:

| Agent | Command | Notes |
|-------|---------|-------|
| Claude Code | `claude` | Default |
| Codex | `codex` | OpenAI |
| OpenClaw | `openclaw` | OpenClaw CLI |
| Custom | Any CLI | Configurable |

## Configuration

Edit `.env` or use presets:

```bash
# Use a preset
hivecmd preset use moonshot-cn
```

## Architecture

- **Leader Agent**: Coordinates the team, spawns workers
- **Worker Agents**: Execute tasks in isolated environments
- **Git Worktree**: Each agent gets its own branch
- **Tmux Session**: Terminal session per agent
- **Inbox**: Inter-agent messaging

## Comparison with ClawTeam

| Feature | ClawTeam | HiveCmd |
|---------|----------|---------|
| Git Worktree | ✅ | ✅ |
| Tmux | ✅ | ✅ |
| Task Dependencies | ✅ | ✅ |
| Web UI | ✅ | ✅ |
| P2P Transport | ✅ | 🟡 |
| Skill Output | ✅ | This skill |
| MCP Integration | ✅ | ❌ |
| Stars | 4,174 | New |

## Tips

1. **Use meaningful names**: Agent names like `backend`, `frontend` help track progress
2. **Set clear tasks**: Task descriptions guide agent behavior
3. **Leverage dependencies**: Blocked tasks auto-unlock when dependencies complete
4. **Use Web UI**: Visualize team progress in real-time
5. **Keep agents focused**: One task per agent at a time works best
