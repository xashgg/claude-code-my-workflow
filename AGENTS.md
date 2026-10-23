# Codex entry point

This repository preserves Pedro Sant'Anna's Claude Code workflow. Before work,
read [the platform bridge](.codex/bridge.md), [CLAUDE.md](CLAUDE.md), and relevant
entries in [MEMORY.md](MEMORY.md). Follow the shared academic procedures through
the bridge; Claude-specific tools, settings, hooks, and model names are not Codex
configuration. Current user instructions take precedence over repository guidance.

Use `$academic-<name>` for this repository's skills. The generated adapters under
`.agents/skills/` read the original `.claude/skills/` definitions. Consult
[the source map](.codex/upstream-map.json) for rule scopes, roles, and exclusions.
Read every unscoped rule at task start and matching scoped rules before touching
their artifacts. This is an instruction-loading protocol, not automatic Claude
rule injection. Recheck applicable scopes when the task changes files or roles.

Preserve `CLAUDE.md` and `.claude/` during compatibility maintenance. Do not add
domain customizations, alter personal settings, change Git remotes, install hooks,
commit, push, or publish without authorization for that action. Maintain existing
quality thresholds and report checks that failed or could not run. Never bypass
a check to make a compatibility result look successful.

## Python environment policy

- Before Python execution, inspect project/skill instructions, existing `.venv`
  or `venv`, dependency specifications, and lockfiles.
- Reuse the project `.venv`, documented virtual environment, or documented Conda
  environment, in that order. Preserve an existing uv workflow.
- Use explicit interpreter paths. Never install into global Python or Conda
  `base`; on this machine `D:\anaconda3\python.exe` is base.
- Standard-library-only utilities need no new environment or package install if
  no project environment is specified. Base Python may bootstrap a `.venv`.
- When third-party dependencies are needed and no suitable environment exists,
  create `.venv` at the project/skill root; install from existing specifications
  inside it. Do not create redundant environments or change dependency managers.
- Do not silently upgrade Python/pip/packages, uninstall dependencies, or replace
  lockfiles. Installation and environment changes need task-specific authorization.

For usage, support limits, validation evidence, and upstream synchronization, read
[the Codex guide](.codex/README.md).
