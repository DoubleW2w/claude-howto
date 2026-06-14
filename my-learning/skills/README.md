# Agent Skills 核心知识

> 用二八法则 + 缺口补全方法论，从 `zh/03-skills/README.md`（887 行）提炼的核心知识。完整教程见 [zh/03-skills/README.md](../../zh/03-skills/README.md)。

> **可视化决策**：生成 5 个 HTML。理由：三层架构/加载流程/类型优先级/调用模式/fork 涉及层级·时序·覆盖·对比·状态隔离，表格讲不清；其余纯配置/决策表用表格。无不确定项。

## 一句话定义

Skill = 可复用、基于文件系统的能力包，按需加载，相关场景自动调用。

## 核心概念

| 概念 | 定义 |
|------|------|
| Skill | 可复用能力包，封装领域知识/工作流/最佳实践 |
| 渐进式披露 | Claude 按需分阶段加载，不一开始塞满上下文 |
| 三层加载 | 元数据 → 指令 → 资源，逐层进入上下文 |

## 三层架构

| 层级 | 加载时机 | token 成本 | 内容 |
|------|----------|-----------|------|
| 第 1 层：元数据 | 始终（启动时） | 每个 skill ~100 tokens | YAML frontmatter 中的 `name` + `description` |
| 第 2 层：指令 | skill 被触发时 | ≤5k tokens | SKILL.md 正文（指令与指导） |
| 第 3 层：资源 | 按需 | 无上限 | 脚本/模板/文档，通过 bash 执行，内容不进上下文 |

可安装大量 Skills 而不担心上下文损耗——触发前 Claude 对每个 skill 只知道"它存在"和"何时使用"。层级·成本·内容是空间维度对比，适合可视化。

> [查看三层架构可视化](assets/skills-three-layers.html)

## 加载流程

1. 用户发请求（如"审查这段代码的安全问题"）
2. Claude 检查已加载的元数据（第 1 层，启动时已就绪）
3. 把请求匹配到某 skill 的 `description`
4. 读该 skill 的 SKILL.md（第 2 层指令进入上下文）
5. 按需读模板/脚本等资源（第 3 层，内容不进上下文）→ 执行

时序与数据流维度，适合可视化。

> [查看加载流程可视化](assets/skills-loading-flow.html)

## 类型与位置

| 类型 | 位置 | 范围 | 是否共享 |
|------|------|------|---------|
| Enterprise（企业级） | Managed settings | 全组织用户 | 是 |
| Personal（个人） | `~/.claude/skills/<name>/SKILL.md` | 个人 | 否 |
| Project（项目） | `.claude/skills/<name>/SKILL.md` | 团队（git 共享） | 是 |
| Plugin（插件） | `<plugin>/skills/<name>/SKILL.md` | 启用范围内 | 视情况 |

同名 skill 优先级：**enterprise > personal > project**。Plugin skill 用 `plugin-name:skill-name` 命名空间，因此不冲突。

支持嵌套目录与 `--add-dir` 自动发现（子目录/额外目录中的 skill 自动加载，支持实时变更检测）。

> [查看类型优先级可视化](assets/skill-type-priority.html)

## 创建 Skill

目录结构：

```text
my-skill/
├── SKILL.md           # 主指令（必需）
├── template.md        # 供 Claude 填写的模板
├── examples/
│   └── sample.md
└── scripts/
    └── validate.sh
```

SKILL.md 必填字段（frontmatter 示例）：

```yaml
---
name: your-skill-name
description: 简要说明这个 Skill 做什么以及何时使用
---
```

- **`name`**：仅小写字母/数字/连字符，≤64 字符，禁含 `anthropic`/`claude`。
- **`description`**：说明做什么 + 何时用，≤1024 字符。**决定 Claude 是否能正确自动触发**——关键。

## frontmatter 可选字段

下表为完整可选字段（必填的 `name`/`description` 见上节）。★ 标高频或常见缺口字段。版本列标引入版本，未标者为基础字段。

| 字段 | 说明 | 版本 |
|------|------|------|
| ★ `argument-hint` | `/` 自动补全菜单中显示的提示，如 `"[filename] [format]"`。 | |
| ★ `disable-model-invocation` | `true` = 只有用户能通过 `/name` 调用；Claude 永不自动调用（处理带副作用的工作流）。 | |
| ★ `user-invocable` | `false` = 从 `/` 菜单隐藏；只有 Claude 能自动调用（背景知识型 skill）。 | |
| ★ `allowed-tools` | 逗号分隔的工具列表，使用这些工具时免权限提示。 | |
| ★ `disallowed-tools` | 逗号分隔的工具列表，skill 激活期间移除这些工具（与 `allowed-tools` 互补）。 | v2.1.152 |
| ★ `model` | skill 激活期间的模型覆盖（如 `opus`、`sonnet`）。 | |
| ★ `effort` | skill 激活期间的 effort 覆盖：`low`/`medium`/`high`/`xhigh`/`max`。可用级别取决于模型（Opus 4.8 默认 `high`）。 | v2.1.120 |
| ★ `context` | `fork` = 在隔离 subagent 上下文中运行，拥有独立上下文窗口，保主对话干净。 | |
| ★ `agent` | `context: fork` 时使用的 subagent 类型（如 `Explore`、`Plan`、`general-purpose`）。 | |
| `shell` | `` !`command` `` 替换与脚本所用 shell：`bash`（默认）或 `powershell`。 | |
| `hooks` | 限定在本 skill 生命周期内的 hooks（格式与全局 hooks 相同）。 | |
| `paths` | 限制 skill 自动激活时机的 glob 模式（逗号分隔字符串或 YAML 列表）。 | |

frontmatter 示例（字段名以上表为准）：

```yaml
---
name: my-skill
description: 这个 skill 做什么以及何时使用
argument-hint: "[filename] [format]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob
disallowed-tools: Write, Edit
model: opus
effort: high
context: fork
agent: Explore
shell: bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
paths: "src/api/**/*.ts"
---
```

## 调用控制 3 模式

两个 frontmatter 字段组合出三种调用模式：

| Frontmatter | 你能调用 | Claude 能调用 |
|-------------|---------|--------------|
| （默认） | 是 | 是 |
| `disable-model-invocation: true` | 是 | 否 |
| `user-invocable: false` | 否 | 是 |

**何时用：**

- **`disable-model-invocation: true`**：副作用 workflow——`/commit`、`/deploy`、`/send-slack-message`。你不想让 Claude 因"代码看起来就绪"就擅自部署。
- **`user-invocable: false`**：背景知识——如 `legacy-system-context` 解释旧系统如何工作，对 Claude 有用，但对用户不是一个有意义的动作。

> [查看调用模式可视化](assets/skill-invocation-modes.html)

## 字符串替换 + 动态注入

Skill 内容在发送给 Claude 之前会被解析替换。支持以下变量：

| 变量 | 说明 |
|------|------|
| `$ARGUMENTS` | 调用 skill 时传入的全部参数。 |
| `$ARGUMENTS[N]` 或 `$N` | 按索引（从 0 开始）访问特定参数。 |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID。 |
| `${CLAUDE_SKILL_DIR}` | 包含该 skill `SKILL.md` 文件的目录。 |
| `${CLAUDE_EFFORT}` | 当前 effort 级别（`low`/`medium`/`high`/`xhigh`/`max`），可据此分支化 skill 行为，如 `[ "${CLAUDE_EFFORT}" = "max" ] && deep_analysis`（v2.1.120+）。 |

最简示例——`/fix-issue 123` 调用时，正文中的 `$ARGUMENTS` 被替换成 `123`：

```yaml
---
name: fix-issue
description: Fix a GitHub issue
---

Fix GitHub issue $ARGUMENTS following our coding standards.
```

**动态上下文注入** `` !`command` ``：在 skill 内容发给 Claude 之前执行 shell 命令，把**输出**内联进来；命令本身不进入上下文，Claude 只看到最终输出。默认在 `bash` 中执行；在 frontmatter 设置 `shell: powershell` 改用 PowerShell。典型用途是注入 PR 上下文：

```yaml
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`
```

## subagent 运行（context: fork）

`context: fork` 让 skill 在隔离的 subagent 上下文中运行——skill 内容成为专用 subagent 的任务，拥有**独立上下文窗口**，从而保持主对话干净。`agent` 字段指定 subagent 类型：

| Agent 类型 | 适用场景 |
|------------|----------|
| `Explore` | 只读研究、代码库分析。 |
| `Plan` | 制定实现计划。 |
| `general-purpose` | 需要全部工具的宽泛任务。 |
| 自定义 agents | 在你的配置中定义的专用 agent。 |

frontmatter 片段：

```yaml
---
context: fork
agent: Explore
---
```

> **v2.1.145 修复**：使用 `context: fork` 的 skill 在少数情况下可能触发无限递归调用循环——编写或依赖 fork 类 skill 请升级到 v2.1.145+。

> [查看 fork context 可视化](assets/skill-fork-context.html)

## 管理 + 权限设置

### 限制 Claude 对 skill 的访问

在 `/permissions` 中用 `Skill` 前缀的规则控制。规则放在 allow 还是 deny 列表决定语义：

```bash
# deny 规则：禁用所有 skills
Skill

# allow 规则：只允许特定 skills（带 * 的为 glob 匹配）
Skill(commit)
Skill(review-pr *)

# deny 规则：拒绝特定 skills
Skill(deploy *)
```

也可逐个隐藏 skill——在其 frontmatter 添加 `disable-model-invocation: true`。

### 控制 skill 覆盖行为（`skillOverrides`）

当项目 skill 与用户 skill 同名时，默认项目胜出（`on`）。`skillOverrides` 设置（v2.1.129+）可调整，写入 `~/.claude/settings.json` 或项目 `.claude/settings.json`：

```json
{
  "skillOverrides": "name-only"
}
```

| 取值 | 行为 |
|------|------|
| `"on"`（默认） | 仓库 skill 可覆盖同名用户 skill。 |
| `"off"` | 完全禁用覆盖——用户 skill 始终胜出。 |
| `"name-only"` | 仅按 skill 名称匹配覆盖（忽略 description / 来源）。 |
| `"user-invocable-only"` | 只有 user-invocable 的 skill 可被覆盖；model 调用的 skill 始终来自原始位置。 |

## 安全设置

**可信来源原则**：skill 通过指令和代码赋予 Claude 能力——恶意 skill 可引导 Claude 以有害方式调用工具或执行代码。**把 skill 当作安装软件对待**，安装前彻底审计 skill 目录中的所有文件；从外部 URL 获取内容的 skill 尤其有风险（来源可能被入侵）。

两个禁用设置（写入 `~/.claude/settings.json` 或项目 `.claude/settings.json`）：

| 设置 | 作用 | 版本 |
|------|------|------|
| `disableSkillShellExecution` | `` !`command` `` 标记作为字面文本保留而非执行——在不禁用 skill 本身的前提下移除 skill 级别 shell 注入攻击面。考虑配合 `allowedTools` 白名单做纵深防御。 | v2.1.91 |
| `disableBundledSkills` | 对模型隐藏 Claude Code 自带的内置 skills、workflows 和 commands——当内置 skill 在某项目里是噪音，或想缩小模型的 skill 范围时使用。 | v2.1.169 |

`disableBundledSkills` 的环境变量等价形式：

```bash
export CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1
```

## 版本演进速查

| 版本 | 变更 |
|------|------|
| v2.1.120 | `${CLAUDE_EFFORT}` 变量；`effort` frontmatter 字段 |
| v2.1.121 | `/skills` 交互菜单可输入筛选 |
| v2.1.129 | `skillOverrides` 设置 |
| v2.1.133 | subagent 通过 Skill tool 发现项目/用户/插件 skill |
| v2.1.145 | `context: fork` 无限递归修复；`/run`、`/verify`、`/run-skill-generator` 内置 skill |
| v2.1.146 | `/simplify` 改名 `/code-review` |
| v2.1.152 | `disallowed-tools` frontmatter；`/reload-skills` 命令 |
| v2.1.169 | `disableBundledSkills` 设置 |

## 三要三不要 + 常见陷阱

| ✅ 要 | ❌ 不要 |
|------|--------|
| description 写具体触发词（加入用户自然说出的关键词） | 省略或写模糊的 description（如 "Helps with documents"） |
| 用 `paths` 限定激活时机（聚焦一种能力） | 把 skill 做得太宽泛（如 "Document processing"） |
| 审计不可信来源 skill（把 skill 当作安装软件对待） | 未审计就装来自不可信来源的 skill |

**常见陷阱：**

- **skill 不触发** → description 加用户自然说出的关键词；先问 "What skills are available?" 确认它会被列出。
- **触发太频繁** → 加 `disable-model-invocation: true`，只允许用户手动调用。
- **看不到全部 skills** → 描述预算超限（上下文窗口的 1%，回退 8,000 字符）。用 `/context` 查被裁剪的 skill；用 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量覆盖预算。

## 延后查阅

以下内容本笔记不展开，链回完整教程：

- **内容类型**：参考型（内联知识：约定/模式/风格指南/领域知识）vs 任务型（分步指令，常用 `/skill-name` 调用）——靠 `description` 控制即可。
- **实战示例 ×6**：代码审查 / 代码库可视化 / 部署 / 品牌语气 / CLAUDE.md 生成 / 重构——见 [zh/03-skills/README.md#实战示例](../../zh/03-skills/README.md#实战示例)。
- **故障排查**：见 [zh/03-skills/README.md#故障排查](../../zh/03-skills/README.md#故障排查)。

## 延伸阅读

- [官方 Skills 文档](https://code.claude.com/docs/en/skills)
- [Agent Skills 架构博客](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)
- [完整教程：zh/03-skills/README.md](../../zh/03-skills/README.md)
- 相关模块：[Memory（02-memory）](../../zh/02-memory/README.md)、[Subagents（04-subagents）](../../zh/04-subagents/README.md)、[Hooks（06-hooks）](../../zh/06-hooks/README.md)

---

**Last Updated**: 2026 年 6 月 14 日
**Claude Code Version**: 2.1.170
**Sources**:
- https://code.claude.com/docs/en/skills
- zh/03-skills/README.md
**Compatible Models**: Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
