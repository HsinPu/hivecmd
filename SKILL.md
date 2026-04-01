# HiveCmd 🤖

AI Agent Swarm Intelligence - Make AI agents work as a team.

## What is HiveCmd?

HiveCmd enables AI agents to collaborate as a coordinated team. The leader agent spawns workers, assigns tasks, and manages coordination.

## Installation

```bash
pip install hivecmd
# or
git clone https://github.com/HsinPu/hivecmd.git
cd hivecmd
pip install -e .
```

## Quick Start

```bash
# Create a team from template
hivecmd templates create webapp my-team

# Or manually
hivecmd team create my-team
hivecmd spawn agent my-team -n worker1 -t "implement auth"

# Monitor
hivecmd board show my-team
hivecmd board serve --port 8080

# Or use AI to auto-create
hivecmd agent config -k YOUR_API_KEY
hivecmd agent create "build a machine learning team"
```

## Commands

| Command | Description |
|---------|-------------|
| `team create/list/show` | Team management |
| `spawn agent/task` | Spawn agents and tasks |
| `board show/serve` | Monitor team status |
| `task list/update` | Task management |
| `inbox send/receive` | Inter-agent messaging |
| `templates list/create` | Team templates |
| `agent create` | AI auto-create team |
| `mcp tools` | MCP server |
| `gource run` | Visualization |
| `lifecycle` | Agent lifecycle hooks |

## Examples

### Web Development Team
```bash
hivecmd templates create webapp my-webapp
```

### Research Team
```bash
hivecmd templates create research my-research
```

### Investment Team
```bash
hivecmd templates create hedge-fund my-fund
```

### AI Auto-Create
```bash
hivecmd agent config -k YOUR_KEY
hivecmd agent create "build a team for machine learning"
```

## Environment Variables

```bash
HIVECMD_LLM_API_KEY=your-api-key
HIVECMD_LLM_MODEL=openai/gpt-4o-mini
```

## Features

- Multi-agent collaboration
- Team templates
- Task dependencies
- Web UI dashboard
- Inter-agent messaging
- Agent lifecycle hooks
- MCP integration
- Git worktree isolation
- Tmux session management

## License

MIT
