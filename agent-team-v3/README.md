# Agent Team v1.0

**Local multi-agent coding system powered by Ollama.**

Specialized agents (Architect, Builder, Critic, Security, Optimizer, Tester, …) collaborate with real **tool use** (read/write files, search, run Python, git, …), session memory, skills, and workflows.

No cloud API keys required – everything runs against your local Ollama instance.

---

## What's new vs the original prototype

| Feature | Before | Now |
|---------|--------|-----|
| Tool use | None | Full local tool loop (files, code exec, git, search) |
| Agents | 8 roles, chat-only | 10 roles + real tool access |
| Collaborate pipeline | Keyword-triggered re-prompts | Full multi-pass with tools + tests |
| Memory | Truncated turns | Persistent session + facts + project file index |
| Skills | Static text | Executable skill runners |
| Workflows | Print node names | Real sequential agent/skill execution |
| Safety | — | Path-traversal protection, command filters, timeouts |
| Tests | None | Unit tests for tools, memory, roster |
| CLI | Basic | Richer commands + `quick` mode |
| Packaging | Minimal | Proper `pyproject.toml`, entry points |

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- Recommended model: `qwen2.5-coder` (or any strong coding model you prefer)

```bash
ollama pull qwen2.5-coder
ollama serve
```

---

## Quick start

```bash
cd agent-team-v3
PYTHONPATH=. python -m team
```

Or install editable:

```bash
pip install -e .
team
```

Inside the REPL:

```
team> check
team> collaborate Build a minimal FastAPI app with JWT auth and a /health endpoint
team> quick Write a pure-python LRU cache with tests
team> workflow run full_dev "Add rate limiting middleware"
team> skill tdd "implement binary search"
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `check` | Verify Ollama connectivity & list models |
| `team` / `show` | Show agent roster |
| `opinion <prompt>` | Every specialist answers independently |
| `fusion <prompt>` | Collect insights → synthesize best solution |
| `collaborate <prompt>` | Full pipeline (plan → build → review → secure → test → polish) |
| `think <prompt>` | Deep research → draft → critique → refine |
| `quick <prompt>` | Fast single-builder path with tools |
| `skill <name> [ctx]` | Run a skill (implement, debug, review, tdd, security, …) |
| `skills` | List skills |
| `workflow list` | List workflows |
| `workflow run <name> [prompt]` | Execute a workflow |
| `memory index` | Rebuild project file index |
| `memory query <term>` | Search indexed files |
| `tools` | Show available tools |
| `config` | Show runtime config |
| `clear` | Reset session memory |
| `help` | Help |
| `exit` | Quit |

---

## Agents

| Name | Role | Tools | Notes |
|------|------|-------|-------|
| architect | Planning | ✓ | Blueprints, risks, layout – no full impl |
| main | Primary builder | ✓ | Production code via `write_file` |
| secondary | Refactorer | ✓ | Alternatives & hardening |
| fusion | Synthesizer | ✓ | Merges viewpoints into final artifact |
| researcher | Analysis | ✓ | Codebase survey & algorithms |
| critic | Quality | ✓ | Scores + mandatory fixes |
| security_auditor | Security | ✓ | OWASP-style audit |
| optimizer | Performance | ✓ | Complexity & bottlenecks |
| tester | Tests | ✓ | Writes & runs tests |
| browser | Automation | ✓ | Playwright / scraping scripts |

---

## Tools available to agents

Agents emit:

```xml
<tool>
name: write_file
path: src/app.py
content: ... full source ...
</tool>
```

Supported tools:

- `list_dir`, `read_file`, `write_file`
- `search_files` (regex + glob)
- `run_python` (sandboxed, timeout)
- `run_shell` (optional, filtered, timeout)
- `git_status`, `git_diff`
- `list_output`, `syntax_check`

Path traversal outside the project root is blocked.

---

## Workflows

- `full_dev` – complete plan → implement → review → secure → test → polish
- `quick_fix` – implement → light review → fix
- `security_pass` – audit → harden → re-audit
- `tdd` – runs the TDD skill

Custom workflows are plain JSON under `workflows/`.

---

## Configuration

Optional `team-config.json` in the project root:

```json
{
  "ollama_host": "http://localhost:11434",
  "default_model": "qwen2.5-coder",
  "max_tool_rounds": 12,
  "allow_shell": true,
  "enable_tools": true,
  "verbose": true
}
```

Environment variables:

- `OLLAMA_HOST`
- `OLLAMA_MODEL`

---

## Project layout

```
agent-team-v3/
├── team/               # core package
│   ├── cli.py
│   ├── runtime.py      # orchestration + tool loop
│   ├── tools.py        # tool registry & parser
│   ├── team.py         # agent definitions
│   ├── memory.py
│   └── config.py
├── skills/             # executable skill prompts
├── workflows/          # JSON pipelines
├── tests/              # unit tests (no Ollama needed)
├── output/             # fallback auto-saved code
└── pyproject.toml
```

---

## Running tests

```bash
pip install pytest
PYTHONPATH=. pytest tests/ -q
```

---

## Tips for best results

1. Prefer **`collaborate`** for non-trivial features – it runs the full quality loop.
2. Prefer **`fusion`** when you want one polished artifact from multiple viewpoints.
3. Use **`quick`** for small, focused tasks.
4. Keep Ollama models with strong coding ability (`qwen2.5-coder`, `deepseek-coder`, `codellama`, etc.).
5. Work inside a real project directory so agents can inspect existing code.
6. After a run, inspect files the agents wrote – they prefer `write_file` over markdown dumps.

---

## License

MIT
