# Platform bridge

The `.claude/` files remain the procedure and reference source of truth. This
file interprets their platform-specific instructions for Codex. It does not
register Claude hooks, grant permissions, or reproduce Claude runtime isolation.

## Loading and invocation

1. Read `CLAUDE.md`, relevant `MEMORY.md` entries, and all unscoped rules listed
   in `upstream-map.json`. Before editing or reviewing an artifact, read rules
   whose scopes match it. Rule paths are relative to the repository root; match
   `**` across zero or more directories. The map retains original scopes.
2. Read a selected original `SKILL.md` in full. Its relative links resolve from
   its own directory, not from the generated adapter. Scripts run from the
   repository root unless the original procedure explicitly changes directory.
3. Interpret `/name` in a procedure as this repository's `$academic-name`, using
   the map to locate its adapter. This is a name translation, not a custom slash
   command registration. An excluded entry has no adapter: report its recorded
   limitation rather than executing it by reading around the exclusion.
4. `$ARGUMENTS` means the user's supplied argument text; `$0`, `$1`, etc. mean
   positional arguments described by the selected skill. Parse flags and paths
   without evaluating them as shell code. Quote paths containing spaces.
5. An explicit-only sibling can contribute procedural instructions to a workflow
   the user authorized, but may not launch a separate task implicitly. Reading
   its file must never bypass its authorization or capability boundaries.

Original YAML is documentation of the Claude contract. Only generated `name`
and `description`, plus supported `agents/openai.yaml` policies, configure the
Codex skill. `allowed-tools`, `disallowed-tools`, `context`, `model`, `effort`,
and `argument-hint` are not equivalent Codex runtime controls.

## Tools and execution

| Original instruction | Codex interpretation |
|---|---|
| Read, Grep, Glob | Available file-reading/search tools; prefer `rg` for searches |
| Write, Edit, MultiEdit | Available patch/file-edit tools within the authorized scope |
| Bash | Available command tool, with syntax chosen for its actual shell |
| WebSearch, WebFetch | Available search/retrieval tools; say when source access is unavailable |
| AskUserQuestion | Available question mechanism; ask in chat if no question tool exists |
| EnterPlanMode / ExitPlanMode | Use actual plan mode if exposed; otherwise present the plan and honor required approval before dependent edits |
| TodoWrite | Available plan tracking, or a checklist in the existing plan/log |
| Agent / Task | Capability-aware role dispatch below; no assumed `subagent_type` API |
| Monitor / TaskOutput / TaskStop | Available process sessions, output polling, and stop controls; preserve exit status and inspect logs |

Never call a tool merely because a Claude document names it. Discover the actual
tools. A missing runtime or mandatory verification produces a blocked or
unverified result, not a PASS. Optional fallbacks are permitted only where the
original procedure allows them and must name their reduced coverage.

The skills `learn`, `new-skill`, `permission-check`, `context-status`,
`promote-memory`, and `oracle-review` are excluded from the Codex baseline.
Do not treat the Oracle CLI's OpenAI target as a cross-vendor review of Codex.

## Roles, independence, and permissions

When a selected procedure calls for delegation and Codex exposes it, read the
corresponding `.claude/agents/<role>.md` and the orchestration references, then
supply the role body, task, inputs, applicable rules, and output contract to an
available subagent. These documents are role instructions, not registered native
Codex agent types. Do not silently replace required reviewers with self-review.
Schedule all required lenses within the available concurrency limit; a missing
lens is not a clean round. Preserve typed findings, quote checks, adjudication,
convergence rules, and the existing findings validator.

Leave the selected model and reasoning settings unchanged. Claude's tier names
and effort pins do not select Codex models. Report when a procedure's model
diversity cannot be established; never claim equivalent review quality or cost.

Report-only means the reviewed artifact stays unchanged; a report may be saved
where the original procedure permits it. Tool-name lists do not enforce this.
Subagents may inherit permissions and conversation history. For an
independence-critical step, inspect the actual context controls and use a neutral
copy containing only necessary material, with prior verdicts, drafts, expected
values, and answer keys withheld as the original fencing rule requires. Prove
these boundaries before calling a result independent. If they cannot be proven,
stop that verification step and label the outcome unverified. A fresh thread,
role prompt, or another model alone is insufficient.

## Windows and Python

Follow the Python environment policy in `AGENTS.md`. The compatibility utilities
use the standard library; they do not install packages. Optional browser QA needs
an existing suitable environment or a separately authorized isolated setup.

Use native PowerShell syntax for native commands. Invoke existing POSIX `.sh`
scripts through a verified Git Bash or WSL environment; do not assume `bash` on
PATH selects Git Bash. Verify `python3` resolves to the intended interpreter
inside that environment. WSL paths and Windows paths are different environments.
Do not change execution policy, global aliases, or personal configuration.

For native Windows TeX, translate shell environment assignments: set `TEXINPUTS`
and `BIBINPUTS` in the child process with Windows `;` search separators and retain
the default TeX search path with a trailing separator. Keep XeLaTeX, BibTeX, and
the original pass sequence. Restore process environment values afterward. Use
the available PDF viewer/inspection tools in place of macOS `open`; distinguish
successful compilation from visual inspection.

## Hooks, state, and quality gates

No lifecycle hooks are wired into Codex by this baseline. Do not report Claude
Git guards, issue guards, claim reconciliation, notifications, automatic logging,
or compaction restoration as active Codex enforcement. Do not read or write
`~/.claude` caches to emulate Codex state. Use the authorized checkpoint/log
procedures in `quality_reports/` and verify saved state when resuming. Never
invent a context percentage from Claude's context-window assumptions.

Run shared quality checks explicitly. The Git pre-commit hook is active only if
the clone is configured to use it; its presence is not proof. Do not install it
or bypass it without authorization. Existing GitHub workflows remain unchanged.
The adapter validator supplements those checks and does not certify runtime
behavior, reviewer independence, or academic correctness.

Commit, push, issue creation, publication, external uploads, mail, and calendar
mutations require authorization for the actual action. A skill name, a request
to review, or a file containing such a step is not blanket authorization.
Retain confidentiality and disclosure restrictions from the canonical rules.
