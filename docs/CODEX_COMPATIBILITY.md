# Claude Code / Codex 兼容性与测试记录

记录日期：2026-10-23。上游审计基线：`ae72617`。这是该次迁移的验证快照，不代表所有功能均已完成端到端验收。

使用方式与上游同步步骤见 [Codex 指南](../.codex/README.md)，平台转换约定见 [bridge](../.codex/bridge.md)，源文件指纹、规则作用域和排除原因见 [source map](../.codex/upstream-map.json)。本文件记录功能差异与测试证据，不复制原 Skill 正文。

## 状态与证据解释

- **保留**：Claude 原始定义及配置保持完整；未进行实际 Claude Code 会话测试。
- **适配**：存在引用原定义的 Codex 适配器；通过发现与结构检查，不等于整个工作流已经运行成功。
- **条件适配**：还依赖外部工具、授权、审阅隔离或其他运行条件；条件未满足时不得给出 PASS。
- **排除**：未提供 Codex 适配器；Claude 原文件仍保留。
- **未接入**：没有在 Codex 中连接相应自动化行为。

下表的 T 编号指向测试记录。没有专项证据的功能均为**端到端未验证**；“保留”也不表示 Claude 运行时已验证。测试通过、结构检查通过、预期失败、已知失败和未验证分别记录。

## 平台机制

| 功能 | Claude Code | Codex | 证据与限制 |
|---|---|---|---|
| 项目入口 | 保留 `CLAUDE.md` | `AGENTS.md` 引导读取原定义与 bridge | T03 验证 bundled engine 自动加载；VS Code GUI 未验证 |
| Skills 发现 | 保留 `.claude/skills/`，61 项 | `.agents/skills/`，55 个引用适配器 | T01、T02；没有复制原工作流正文 |
| 显式调用 | 原 `/name` 约定 | `$academic-name` | T04 仅验证一个 Skill 的显式调用和引用加载 |
| YAML frontmatter | 保留 Claude 字段 | 转换必要元数据，其他行为由 bridge 约束 | 不把工具白名单、context fork、model/effort 字段当作 Codex 权限 |
| 禁止隐式触发 | 保留原声明 | 19 项有 `allow_implicit_invocation: false` 策略文件 | T01 检查文件；运行时是否阻止隐式触发未验证 |
| 路径规则 | 保留 37 个规则文件 | 根据 map 显式读取无作用域及匹配作用域规则 | 没有复现 Claude 自动注入机制；遵从效果未逐项测试 |
| 自定义 Agent | 保留 18 个角色 | 可复用角色正文，未注册原生自定义 Agent 配置 | 全部角色执行未验证；权限限制不能仅靠角色提示等价实现 |
| 多 Agent 与独立审阅 | 保留原流程 | 依赖可用子 Agent 工具及可证明的隔离 | 干净历史、文件隔离、隐藏先前结论均未完成运行验证 |
| 模型与 effort 路由 | 保留原模型设置 | 保留用户选择；不转换 Claude 模型档位 | 质量、成本和多模型独立性没有等价保证 |
| 生命周期 Hooks | 保留 `.claude/settings.json` 与原 Hooks | 未接入 | T06 是合成脚本测试，不是平台事件测试 |
| 上下文、自动记忆、状态栏 | 保留原 Claude 机制 | 不读取 Claude 私有状态冒充 Codex 状态 | 相关专用 Skills 排除；检查点可按授权手动记录 |
| 外部工具、连接器与发送 | 保留流程定义 | 依赖实际工具、认证和任务授权 | 未测试外发、上传、发布、MCP 或邮件工作流 |
| Python / R / Stata | 保留原脚本 | 可复用可执行脚本，需相应环境 | Python 标准库测试通过；R / Stata 工作流未运行 |
| LaTeX / Quarto | 保留原编译流程 | 可调用本机工具链 | T07、T08 为复制样例的工具链烟雾测试 |
| 质量门禁 | 保留原阈值与脚本 | 显式执行共享门禁 | T05 通过；不等于生命周期自动执行 |
| Git pre-commit | 保留 `.githooks/pre-commit` | 同一个 Git 机制 | 本机未安装：`core.hooksPath` 未设置且无 `.git/hooks/pre-commit` |
| CI | 保留既有 workflows | 新增 Windows / Ubuntu 适配器检查 | 配置已提供；远程 GitHub Actions 尚未执行 |
| Windows 与链接 | 保留原文件布局 | 使用普通文件和相对引用，不依赖 symlink | `core.symlinks=false`；T01 跨平台通过；CRLF 限制见 T09 |
| 输出风格 | 保留 `.claude/output-styles/` | 没有自动导入 Claude 输出风格的适配 | 未验证等价行为 |

## Skills：逐项记录

所有原始路径为 `.claude/skills/<名称>/SKILL.md`；适配路径为 `.agents/skills/academic-<名称>/SKILL.md`。所有 Claude 列的“保留”均只表示原配置保留。所有“适配”项具有 T01 结构与 T02 发现证据；下列专项证据不会扩大为完整工作流验收。

`显式` 表示有禁止隐式调用的策略文件；`隔离` 表示原流程要求的独立审阅条件仍须验证。

| Skill（原定义） | Claude Code | Codex | 专项测试 / 限制 |
|---|---|---|---|
| [adjudicate-review](../.claude/skills/adjudicate-review/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [audit-reproducibility](../.claude/skills/audit-reproducibility/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [blast-radius](../.claude/skills/blast-radius/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [capture-environment](../.claude/skills/capture-environment/SKILL.md) | 保留 | 适配 | 未安装依赖；不改变全局或 Conda base 环境 |
| [challenge](../.claude/skills/challenge/SKILL.md) | 保留 | 适配 | 端到端未验证；显式 |
| [checkpoint](../.claude/skills/checkpoint/SKILL.md) | 保留 | 适配 | 端到端未验证；显式 |
| [coauthor-brief](../.claude/skills/coauthor-brief/SKILL.md) | 保留 | 适配 | 端到端未验证；显式 |
| [commit](../.claude/skills/commit/SKILL.md) | 保留 | 适配 | 未提交或推送；Git 写操作需任务授权 |
| [compile-latex](../.claude/skills/compile-latex/SKILL.md) | 保留 | 适配 | T07：仅工具链样例，未执行完整 Skill |
| [compress-session](../.claude/skills/compress-session/SKILL.md) | 保留 | 适配 | 端到端未验证；显式 |
| [context-status](../.claude/skills/context-status/SKILL.md) | 保留 | 排除 | 依赖 Claude 上下文/cache 遥测 |
| [create-lecture](../.claude/skills/create-lecture/SKILL.md) | 保留 | 适配 | 端到端未验证；显式 |
| [credible-claims](../.claude/skills/credible-claims/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [data-analysis](../.claude/skills/data-analysis/SKILL.md) | 保留 | 适配 | R / Stata 等实际分析未验证 |
| [data-management-plan](../.claude/skills/data-management-plan/SKILL.md) | 保留 | 条件适配 | 端到端未验证；显式、隔离 |
| [deep-audit](../.claude/skills/deep-audit/SKILL.md) | 保留 | 条件适配 | 端到端未验证；显式、隔离 |
| [deploy](../.claude/skills/deploy/SKILL.md) | 保留 | 适配 | 发布、推送及部署未执行 |
| [devils-advocate](../.claude/skills/devils-advocate/SKILL.md) | 保留 | 适配 | T04：显式调用与原定义加载；未执行完整审阅 |
| [diagnose](../.claude/skills/diagnose/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [differential-audit](../.claude/skills/differential-audit/SKILL.md) | 保留 | 条件适配 | 端到端未验证；隔离 |
| [disclosure-check](../.claude/skills/disclosure-check/SKILL.md) | 保留 | 适配 | 端到端未验证；显式 |
| [extract-tikz](../.claude/skills/extract-tikz/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [grant-proposal](../.claude/skills/grant-proposal/SKILL.md) | 保留 | 条件适配 | 端到端未验证；显式、隔离 |
| [humanize](../.claude/skills/humanize/SKILL.md) | 保留 | 适配 | 端到端未验证；显式 |
| [interview-me](../.claude/skills/interview-me/SKILL.md) | 保留 | 条件适配 | 端到端未验证；隔离 |
| [issues](../.claude/skills/issues/SKILL.md) | 保留 | 适配 | 真实 issue 写入未执行 |
| [learn](../.claude/skills/learn/SKILL.md) | 保留 | 排除 | 编写并注册 Claude Skills，尚未转换；显式 |
| [lit-review](../.claude/skills/lit-review/SKILL.md) | 保留 | 条件适配 | 端到端未验证；隔离 |
| [new-diagram](../.claude/skills/new-diagram/SKILL.md) | 保留 | 适配 | 端到端未验证；显式 |
| [new-skill](../.claude/skills/new-skill/SKILL.md) | 保留 | 排除 | 生成 Claude Skill 及其配套文档，尚未转换；显式 |
| [oracle-review](../.claude/skills/oracle-review/SKILL.md) | 保留 | 排除 | 从 Codex 调用 OpenAI 不保留原跨供应商审阅独立性；显式 |
| [pedagogy-review](../.claude/skills/pedagogy-review/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [permission-check](../.claude/skills/permission-check/SKILL.md) | 保留 | 排除 | 依赖 Claude 权限层级 |
| [power-analysis](../.claude/skills/power-analysis/SKILL.md) | 保留 | 适配 | 端到端未验证；显式 |
| [preregister](../.claude/skills/preregister/SKILL.md) | 保留 | 适配 | 端到端未验证；显式 |
| [promote-memory](../.claude/skills/promote-memory/SKILL.md) | 保留 | 排除 | 依赖 Claude 自动记忆及 council；显式 |
| [proofread](../.claude/skills/proofread/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [qa-quarto](../.claude/skills/qa-quarto/SKILL.md) | 保留 | 条件适配 | 浏览器 / Playwright 视觉 QA 未验证；隔离 |
| [r-package-check](../.claude/skills/r-package-check/SKILL.md) | 保留 | 适配 | R 包构建与检查未运行；显式 |
| [replication-package](../.claude/skills/replication-package/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [research-ideation](../.claude/skills/research-ideation/SKILL.md) | 保留 | 条件适配 | 端到端未验证；隔离 |
| [respond-to-eval](../.claude/skills/respond-to-eval/SKILL.md) | 保留 | 条件适配 | 端到端未验证；隔离 |
| [respond-to-referees](../.claude/skills/respond-to-referees/SKILL.md) | 保留 | 条件适配 | 端到端未验证；隔离 |
| [review-paper](../.claude/skills/review-paper/SKILL.md) | 保留 | 条件适配 | 端到端未验证；隔离 |
| [review-r](../.claude/skills/review-r/SKILL.md) | 保留 | 适配 | Rscript 不在已检查 PATH；未运行 |
| [scaffold-exercises](../.claude/skills/scaffold-exercises/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [seven-pass-review](../.claude/skills/seven-pass-review/SKILL.md) | 保留 | 条件适配 | 端到端未验证；隔离 |
| [simulation-study](../.claude/skills/simulation-study/SKILL.md) | 保留 | 适配 | 端到端未验证；显式 |
| [slide-excellence](../.claude/skills/slide-excellence/SKILL.md) | 保留 | 条件适配 | 端到端未验证；隔离 |
| [stata-replication](../.claude/skills/stata-replication/SKILL.md) | 保留 | 适配 | Stata 不在已检查 PATH；未运行；显式 |
| [submission-disclosures](../.claude/skills/submission-disclosures/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [syllabus](../.claude/skills/syllabus/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [teach-from-paper](../.claude/skills/teach-from-paper/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [translate-to-quarto](../.claude/skills/translate-to-quarto/SKILL.md) | 保留 | 适配 | T08：仅 Quarto 渲染样例；未验证翻译完整性 |
| [triage-inbox](../.claude/skills/triage-inbox/SKILL.md) | 保留 | 适配 | 端到端未验证；显式 |
| [vaccinate](../.claude/skills/vaccinate/SKILL.md) | 保留 | 适配 | 端到端未验证；显式 |
| [validate-bib](../.claude/skills/validate-bib/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [verify-artifact](../.claude/skills/verify-artifact/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [verify-claims](../.claude/skills/verify-claims/SKILL.md) | 保留 | 条件适配 | 端到端未验证；隔离 |
| [visual-audit](../.claude/skills/visual-audit/SKILL.md) | 保留 | 适配 | 端到端未验证 |
| [voice-profile](../.claude/skills/voice-profile/SKILL.md) | 保留 | 条件适配 | 端到端未验证；显式、隔离 |

## Agents：逐项记录

原角色正文可作为任务输入复用，但没有将 Claude 工具权限或模型路由转换为 Codex 强制配置。以下角色均未完成 Codex 角色运行测试；T01 仅校验源清单、引用和变更检测。

| Agent（原定义） | Claude Code | Codex | 测试与限制 |
|---|---|---|---|
| [beamer-translator](../.claude/agents/beamer-translator.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [claim-verifier](../.claude/agents/claim-verifier.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [domain-referee](../.claude/agents/domain-referee.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [domain-reviewer](../.claude/agents/domain-reviewer.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [editor](../.claude/agents/editor.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [humanize-auditor](../.claude/agents/humanize-auditor.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [methods-referee](../.claude/agents/methods-referee.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [pedagogy-reviewer](../.claude/agents/pedagogy-reviewer.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [promote-memory-council](../.claude/agents/promote-memory-council.md) | 保留 | 排除 | Claude 自动记忆流程未迁移 |
| [proofreader](../.claude/agents/proofreader.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [quarto-critic](../.claude/agents/quarto-critic.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [quarto-fixer](../.claude/agents/quarto-fixer.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [r-package-reviewer](../.claude/agents/r-package-reviewer.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [r-reviewer](../.claude/agents/r-reviewer.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [sim-reviewer](../.claude/agents/sim-reviewer.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [slide-auditor](../.claude/agents/slide-auditor.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [tikz-reviewer](../.claude/agents/tikz-reviewer.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |
| [verifier](../.claude/agents/verifier.md) | 保留 | 条件复用角色正文 | T01 结构检查；角色执行、权限与独立性未验证 |

## Hooks：逐项记录

Claude 列仅表示原 Hook 与配置未改动，**未验证 Claude 实际触发**。Codex 没有接入这些 Hook；手动执行脚本不能证明自动拦截、通知或恢复有效。

| Hook | Claude Code | Codex | 测试结果 |
|---|---|---|---|
| [claim-reconcile.py](../.claude/hooks/claim-reconcile.py) | 保留 | 未接入 | T06 合成测试覆盖；平台触发未验证 |
| [context-monitor.py](../.claude/hooks/context-monitor.py) | 保留 | 未接入 | 无该 Hook 专项运行证据；平台触发未验证 |
| [git-guardrails.py](../.claude/hooks/git-guardrails.py) | 保留 | 未接入 | T06 合成测试覆盖；平台触发未验证 |
| [issue-guard.py](../.claude/hooks/issue-guard.py) | 保留 | 未接入 | T06 合成测试覆盖；平台触发未验证 |
| [log-reminder.py](../.claude/hooks/log-reminder.py) | 保留 | 未接入 | 无该 Hook 专项运行证据；平台触发未验证 |
| [notify.sh](../.claude/hooks/notify.sh) | 保留 | 未接入 | 无该 Hook 专项运行证据；平台触发未验证 |
| [open-issues.py](../.claude/hooks/open-issues.py) | 保留 | 未接入 | T06 合成测试覆盖；平台触发未验证 |
| [post-compact-restore.py](../.claude/hooks/post-compact-restore.py) | 保留 | 未接入 | 无该 Hook 专项运行证据；平台触发未验证 |
| [pre-compact.py](../.claude/hooks/pre-compact.py) | 保留 | 未接入 | 无该 Hook 专项运行证据；平台触发未验证 |
| [root-of-trust-guard.py](../.claude/hooks/root-of-trust-guard.py) | 保留 | 未接入 | T06 合成测试覆盖；平台触发未验证 |
| [session-handoff.py](../.claude/hooks/session-handoff.py) | 保留 | 未接入 | T06 合成测试覆盖；平台触发未验证 |

## Rules：逐项记录

以下规则在 Claude 下均保留，在 Codex 下均通过 map 和入口指令按需读取。T01 覆盖清单与源漂移检测；**各规则的实际遵从与 Claude 自动注入均未逐项验证**。原作用域以 map 为准，此表不重新定义作用域。

| 规则 | Claude Code | Codex | 测试 |
|---|---|---|---|
| [agent-authored-code](../.claude/rules/agent-authored-code.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [beamer-quarto-sync](../.claude/rules/beamer-quarto-sync.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [confidential-data](../.claude/rules/confidential-data.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [content-invariants](../.claude/rules/content-invariants.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [cross-artifact-review](../.claude/rules/cross-artifact-review.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [exploration-fast-track](../.claude/rules/exploration-fast-track.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [exploration-folder-protocol](../.claude/rules/exploration-folder-protocol.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [inference-robustness](../.claude/rules/inference-robustness.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [issue-ledger](../.claude/rules/issue-ledger.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [knowledge-base-template](../.claude/rules/knowledge-base-template.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [meta-governance](../.claude/rules/meta-governance.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [model-routing](../.claude/rules/model-routing.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [no-pause-beamer](../.claude/rules/no-pause-beamer.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [orchestrator-protocol](../.claude/rules/orchestrator-protocol.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [orchestrator-research](../.claude/rules/orchestrator-research.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [pdf-processing](../.claude/rules/pdf-processing.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [plan-first-workflow](../.claude/rules/plan-first-workflow.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [post-flight-verification](../.claude/rules/post-flight-verification.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [progress-reports](../.claude/rules/progress-reports.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [prompt-shaping](../.claude/rules/prompt-shaping.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [proofreading-protocol](../.claude/rules/proofreading-protocol.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [quality-gates](../.claude/rules/quality-gates.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [r-code-conventions](../.claude/rules/r-code-conventions.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [r-package-conventions](../.claude/rules/r-package-conventions.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [replication-protocol](../.claude/rules/replication-protocol.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [repo-hygiene](../.claude/rules/repo-hygiene.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [review-fencing](../.claude/rules/review-fencing.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [session-logging](../.claude/rules/session-logging.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [simulation-conventions](../.claude/rules/simulation-conventions.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [single-source-of-truth](../.claude/rules/single-source-of-truth.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [stata-code-conventions](../.claude/rules/stata-code-conventions.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [summary-parity](../.claude/rules/summary-parity.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [tikz-measurement](../.claude/rules/tikz-measurement.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [tikz-prevention](../.claude/rules/tikz-prevention.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [tikz-visual-quality](../.claude/rules/tikz-visual-quality.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [verification-protocol](../.claude/rules/verification-protocol.md) | 保留 | 显式读取适配 | T01；行为未验证 |
| [writing-with-ai](../.claude/rules/writing-with-ai.md) | 保留 | 显式读取适配 | T01；行为未验证 |

## 测试记录

以下运行证据来自 2026-10-23 迁移验证。Codex 引擎为 VS Code 扩展 `26.930.61225` 内置的 `0.160.1`，通过 app-server stdio 探测；不是 VS Code GUI 操作。另有 npm CLI `0.154.0`，不应混淆版本。Python 原生测试使用 Windows Python 3.13.9；Linux 测试使用现有 Ubuntu WSL 的 Python。没有安装依赖。

| 编号 | 测试与环境 | 结果 | 能证明什么 / 不能证明什么 |
|---|---|---|---|
| T01 | `codex-compat.py --check` 与 `test-codex-compat.py`，Windows / Ubuntu WSL | 通过；两平台各 23 个单元测试 | 61 Skills、18 Agents、37 Rules、11 Hooks 清单；55 适配器、19 策略；漂移、幂等、保留原件、未知元数据/工具、CRLF、跨平台排序与输出路径安全。不能证明完整学术流程可用 |
| T02 | bundled engine `skills/list`，按本仓库路径筛选 | 通过：55 个本地 Skills，全部 enabled，无解析错误 | 六个排除项未生成；返回值不提供隐式触发策略执行证据 |
| T03 | 新建临时只读线程，无 Skill 输入、禁止文件工具 | 通过：返回入口标题、`$academic-` 前缀和禁止 base 安装政策；无实际工具事件 | 验证此次引擎自动加载项目入口；未测试 GUI |
| T04 | 临时只读线程显式调用 `$academic-devils-advocate` | 通过：读到原 Skill 标题与 bridge，识别工具授权和自动 Hooks 不等价 | 仅集成探针；没有真实幻灯片审阅或全部 55 项显式调用验收 |
| T05 | `bash scripts/backtest.sh`，临时 Linux LF checkout，包含候选改动 | 全套通过 | surface-sync、skill-integrity、model-versions、links、spec-conformance、staleness、repo-hygiene、derived-counts、ledger-coverage、hook-battery 及 findings validator；实际仓库索引未改动 |
| T06 | T05 中的 hook-battery | 312 个合成用例通过 | 脚本逻辑证据；不证明 Claude / Codex 事件实际接线 |
| T07 | 复制 `HelloWorld.tex` 和参考文献；Windows XeLaTeX → BibTeX → XeLaTeX ×2 | 正例通过：4 页 PDF、0 未定义引用、0 overfull boxes；注入未定义控制命令后预期失败，exit 1 | 编译工具链与负例检测有效；未做视觉检查，也不是 Skill 端到端测试 |
| T08 | 复制 `HelloWorld.qmd` 与主题；Windows Quarto 渲染 | 通过：exit 0，检查 HTML 内容和 reveal 标记 | 不证明视觉保真、浏览器 QA 或发布成功 |
| T09 | WSL 直接执行 Windows CRLF `.sh` | 已知失败：`pipefail` 等被 CRLF 破坏 | T05 使用独立 LF checkout 才通过；没有更改真实仓库行尾或全局 Git 配置 |
| T10 | 原始 tracked 文件对比 HEAD（归一化行尾）；Git 状态检查 | 通过：Claude 文件未改；上游文件仅 hygiene allowlist 增加两行 | 历史、remotes 和真实索引保留；没有实际执行上游合并演练 |
| T11 | GitHub Actions、Claude 会话、GUI、多 Agent 独立审阅、R/Stata、连接器、视觉 QA | 未验证 | 不以文件存在、结构通过或单个探针代替运行证据 |

### 已知环境边界

- `Rscript`、Stata 不在本次检查的 PATH；这不证明机器上未安装它们。
- 本机有 TeX Live 2026 与 Quarto；跨机器仍需检查可执行文件、字体、包与路径。
- PowerShell 的 `codex.ps1` 受执行策略限制；`codex.cmd` 可运行。未修改执行策略。
- Python 测试仅使用标准库，没有新建环境或向 Conda base 安装包。后续若需要第三方依赖，遵循项目环境政策。
- 原生 Windows 的 shell 别名、CRLF 和 Bash 路径不能直接视为 Linux 环境；优先在独立 LF checkout 验证共享 shell 门禁。

## 如何更新本记录

1. 上游更新后先查看 `.claude/`、共享参考文档和脚本差异，再运行只读 `scripts/codex-compat.py --check`。新增或移除组件须重新分类，不能仅生成文件就标记支持。
2. 获得相应修改授权后更新生成器并生成适配器；运行适配器测试及共享门禁。不要手工复制原 Skill 正文，不要覆盖未知文件或删除原配置。
3. 对受影响功能记录日期、源提交、客户端/引擎版本、操作、预期结果、实际结果及证据范围。旧通过记录保留为历史；源变更后先标记“需重验”。
4. 分开记录结构、脚本、平台集成和学术产出验收。真实 Claude 会话、独立审阅或外部工具没测过，继续标记未验证。
5. 禁止以跳过门禁、禁用 Hook 或安装到全局环境来获得通过结果。提交、推送、发布及更改 remotes 仍需要相应授权。

复查命令（使用按项目政策选择的 Python 解释器；下例 `$ProjectPython` 必须先指向该解释器）：

```powershell
& $ProjectPython -B scripts/codex-compat.py --check
& $ProjectPython -B scripts/test-codex-compat.py
```

共享门禁在具备依赖且行尾为 LF 的 Linux checkout 中运行：

```bash
bash scripts/backtest.sh
```

本记录新增的 Markdown 文件不改变适配器源定义；本次文档检查结果以实际检查输出及交付说明为准，不倒填为上述历史运行测试。
