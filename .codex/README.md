# Codex compatibility

Open this repository in the Codex VS Code extension and start a fresh session.
Codex reads [AGENTS.md](../AGENTS.md); the adapters load the original Claude
procedures through [bridge.md](bridge.md). No personal Codex settings are needed.

Mention a repository skill with `$`, for example:

```text
$academic-compile-latex HelloWorld
$academic-proofread Slides/HelloWorld.tex
$academic-review-r scripts/R/03_analyze.R
```

Use the skill selector to confirm the `academic-` entry comes from this checkout.
Restart the session if new skills do not appear. The prefix avoids ambiguity with
similarly named personal skills. Arguments are prompt inputs, not shell commands.

Claude Code continues using its original configuration and `/compile-latex`,
`/proofread`, etc. See [the existing README](../README.md) for Claude setup.

## How the layer works

Adapters contain discovery metadata, a source fingerprint, argument information,
and links. They read the original skill body; supporting references and scripts
stay in their existing locations. Generated files are checked into Git, so a
Windows checkout needs no symlinks, setup command, or generation step to discover
them. Source hashes normalize line endings to LF.

[upstream-map.json](upstream-map.json) records all reviewed skills, agents, rules,
hooks, shared inputs, exclusions, and original rule scopes. It is an inventory,
not Codex configuration. The generator recognizes only the frontmatter syntax
currently reviewed in this repository and rejects unfamiliar syntax or keys.

The only change to an upstream-owned file is the addition of `AGENTS.md`,
`.agents`, and `.codex` to the allowlists in
[check-repo-hygiene.py](../scripts/check-repo-hygiene.py). Its other checks and
all Claude configuration remain intact. Existing public skill counts still
describe `.claude/skills/`; Codex adapters are not additional canonical skills.

## Support boundaries

| Feature | Baseline support |
|---|---|
| Repository instructions and skills | Native discovery entry points, with reference adapters |
| Explicit-only skills | Policy files and adapter instructions provided; installed-client implicit-trigger enforcement remains unverified |
| Academic procedures, references, schemas | Reused from their original files |
| Claude agent roles | Instructions passed to available Codex subagents; no native custom-agent registration |
| Path-scoped rules | Explicit reading through the source map; no automatic Claude rule injection |
| Tool allowlists / report-only roles | Behavioral instructions; no equivalent permission enforcement claimed |
| Independent verification | Requires proven context isolation and a neutral filesystem; otherwise unverified |
| Model/effort routing | Current Codex settings retained; Claude tiers are not translated |
| Shared quality gates | Run explicitly; unchanged upstream CI remains in place |
| Git pre-commit hook | Works only after separately authorized per-clone activation |
| Lifecycle hooks, automatic memory, context estimates | No Codex integration in this baseline |
| R, Stata, TeX, Quarto, browser QA | Conditional on an available, verified runtime/environment |
| Email/calendar and external services | Conditional on session tools and authorization |
| Claude skill evaluation harness | Remains Claude-only; not a Codex evaluation |

Six workflows are deliberately excluded: `context-status`, `permission-check`,
`promote-memory`, `learn`, `new-skill`, and `oracle-review`. Their reasons are in
the source map. A workflow that references an excluded step must report the
limitation rather than execute around it. Inclusion of another adapter does not
certify all of its modes: mandatory unavailable checks block verification.

Use authorized checkpoints and session logs under `quality_reports/` for manual
handoffs. No Claude session-cache files are used to imitate Codex context state.

## Validate or regenerate

Select an explicit Python interpreter using the policy in `AGENTS.md`. These
utilities require only the standard library; no package installation or new
environment is necessary solely for them. In PowerShell, with `$projectPython`
set to that interpreter's path:

```powershell
& $projectPython -B scripts/codex-compat.py --check
& $projectPython -B scripts/test-codex-compat.py
```

After reviewing upstream changes:

```powershell
& $projectPython -B scripts/codex-compat.py --generate
& $projectPython -B scripts/codex-compat.py --check
```

`--check` writes nothing. `--generate` updates only owned generated files and
never deletes files. Review newly added/removed/renamed components and update the
reviewed inventory and exclusions in the generator before enabling them. Inspect
unexpected adapter files yourself; remove an obsolete generated file only after
review. Do not hand-edit generated adapters or the source map.

Run the unchanged full upstream suite through a verified POSIX environment:

```bash
bash scripts/backtest.sh
```

On Windows, explicitly select Git Bash or WSL and verify its `python3`. The
WindowsApps aliases may select another environment or have no interpreter.
See the bridge for native Windows TeX environment syntax. Browser QA uses the
original `SLIDE_QA_PYTHON` mechanism; install nothing into Conda base.

The separate [Codex CI workflow](../.github/workflows/codex-compat.yml) checks
generation and standard-library tests on Windows and Linux. It does not perform
authenticated Codex/Claude sessions, install research dependencies, or publish.

## Incorporate upstream updates

Start with a clean tree and preserve unfinished work. The following are manual
maintenance commands, not actions performed by the compatibility layer:

```bash
git fetch upstream
git switch main
git switch -c sync-upstream-YYYYMMDD
git merge upstream/main
```

Review upstream skills, agents, rules, settings, and scripts; update the reviewed
inventory when necessary, regenerate, and run both suites. Submit the integration
branch through the usual PR process. Keep normal merge history; do not force-push
shared history. No remote changes are needed. Reconcile the small hygiene
allowlist patch if upstream edits the same area. Inspect source changes even when
Git merges cleanly: reference reuse reduces textual conflicts, not behavioral drift.

## Evidence and remaining verification

Validation on 2026-10-23:

- The VS Code extension's bundled Codex engine (`0.160.1`) discovered all 55
  repository adapters as enabled, without skill parsing errors. Global skills
  were filtered by source path rather than counted as repository adapters.
- An ephemeral read-only Codex turn explicitly invoked
  `$academic-devils-advocate`, loaded its canonical source, returned its exact
  heading, and correctly described argument mapping and inactive hooks.
- A separate fresh Codex session returned the exact repository `AGENTS.md`
  heading, skill prefix, and Conda installation restriction without file/tool
  calls. This demonstrates automatic instruction loading in the bundled engine.
- All 23 compatibility tests passed under native Windows Python and Ubuntu WSL.
- The full unchanged upstream backtest passed in a disposable Linux checkout,
  including all 312 hook-battery cases. The new paths were tracked in that copy.
- Copied `HelloWorld.tex` compiled using XeLaTeX/BibTeX/XeLaTeX/XeLaTeX to four
  PDF pages with zero undefined citations and zero overfull boxes. A seeded
  undefined TeX command failed as expected. Copied `HelloWorld.qmd` rendered
  successfully, and its HTML contents were checked. Nothing was published.

The existing CRLF shell scripts fail when run directly from this Windows
checkout under WSL. Gate validation used an LF copy without changing this
checkout's line endings or Git configuration. For WSL maintenance, use a separate
Linux checkout with LF shell scripts; validate the candidate files there.

The app-server skill listing does not expose invocation policy, so the 19 policy
files passing structural checks is not proof of implicit-trigger enforcement.
GUI selector behavior, actual Claude runtime execution, GitHub Actions execution,
browser layout QA, R/Stata execution, connectors, and reviewer independence remain
unverified. The instruction-loading probe exercised the bundled engine through
its app-server interface, rather than inspecting the VS Code GUI. A completed
model response alone is not proof of any of the remaining properties.

Generation and structural checks do not certify academic correctness. The
compatibility tests include deliberately broken inputs and source-preservation
checks; see [the tests](../scripts/test-codex-compat.py) for their exact scope.

Official capability references (checked 2026-10-23):
[instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[skills and invocation policy](https://learn.chatgpt.com/docs/build-skills),
[subagents and inherited permissions](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[hooks and trust](https://learn.chatgpt.com/docs/hooks).
