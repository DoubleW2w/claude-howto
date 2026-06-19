# Hooks 核心知识

> 用二八法则 + 缺口补全方法论，从 `zh/06-hooks/README.md`（1467 行）提炼的核心知识。完整教程见 [zh/06-hooks/README.md](../../zh/06-hooks/README.md)。

> **可视化决策**：生成 6 个 HTML。理由：配置嵌套/退出码三态/I/O 数据流/事件时序/类型对比/组件作用域 涉及层级·状态·数据流·时序·对比·空间，表格讲不清；其余纯配置/决策表用表格。无不确定项。

## 一句话定义

Hook = 会话特定事件触发时自动执行的脚本，接收 JSON 输入（stdin），退出码 + JSON 输出（stdout）返回结果。

## 核心概念

| 概念 | 定义 |
|------|------|
| Hook | 事件触发 + JSON 契约驱动的动作（5 种类型：command/http/prompt/mcp_tool/agent） |
| 事件驱动 | 30 个事件（PreToolUse/PostToolUse/Stop/SessionStart...），按事件自动触发 |
| JSON 契约 | stdin 接收 JSON，stdout 返回 JSON + 退出码；不读命令行参数 |

## 配置结构

配置是四层嵌套：`hooks`（顶层）→ `"EventName"`（事件数组）→ 数组元素（含 `matcher` + `hooks`）→ `hooks` 数组（每个含 `type`/`command`/`timeout`）。

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

**关键字段：**

| 字段 | 说明 | 示例 |
|------|------|------|
| `matcher` | 匹配工具名称的模式（区分大小写） | `"Write"` |
| `hooks` | hook 定义数组 | `[{ "type": "command", ... }]` |
| `type` | Hook 类型：`command`/`prompt`/`http`/`mcp_tool`/`agent` | `"command"` |
| `command` | 要执行的 shell 命令 | `"$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh"` |
| `timeout` | 可选超时时间，单位秒（默认 60） | `30` |
| `once` | 若为 `true`，该 hook 每个会话只运行一次 | `true` |

**Matcher 模式：**

| 模式 | 说明 | 示例 |
|------|------|------|
| 精确字符串 | 匹配特定工具 | `"Write"` |
| 正则表达式 | 匹配多个工具 | `"Edit\|Write"` |
| 通配符 | 匹配所有工具 | `"*"` 或 `""` |
| MCP 工具 | server 和工具模式 | `"mcp__memory__.*"` |

**InstructionsLoaded 的 matcher 取值：**

| Matcher 取值 | 说明 |
|--------------|------|
| `session_start` | 会话启动时加载指令 |
| `nested_traversal` | 嵌套目录遍历时加载指令 |
| `path_glob_match` | 通过路径 glob 模式匹配加载指令 |

嵌套层级适合可视化。

> [查看配置结构可视化](assets/hooks-config-structure.html)

## 配置位置

| 位置 | 作用域 | 是否共享 |
|------|--------|----------|
| `~/.claude/settings.json` | 用户（所有项目） | 否 |
| `.claude/settings.json` | 项目（团队） | 是（git） |
| `.claude/settings.local.json` | 本地项目 | 否（不提交） |
| Managed policy | 组织级 | 是 |
| Plugin `hooks/hooks.json` | 插件作用域 | 视情况 |
| Skill/Agent frontmatter | 组件生命周期 | 视情况 |

## 退出码

| 退出码 | 含义 | 行为 |
|--------|------|------|
| **0** | 成功 | 继续，解析 JSON stdout |
| **2** | 阻断性错误 | 阻断操作，stderr 作为错误展示 |
| **其他** | 非阻断性错误 | 继续，stderr 在 verbose 模式展示 |

三态行为差异是核心控制机制，适合可视化。

> [查看退出码可视化](assets/hooks-exit-codes.html)

## JSON 输入/输出

**stdin 字段：**

| 字段 | 说明 |
|------|------|
| `session_id` | 唯一会话标识符 |
| `transcript_path` | 对话记录文件路径 |
| `cwd` | 当前工作目录 |
| `hook_event_name` | 触发该 hook 的事件名 |
| `tool_name` | 工具名 |
| `tool_input` | 工具参数 |
| `tool_use_id` | 工具调用唯一标识符 |
| `agent_id` | 运行该 hook 的 agent 标识符 |
| `agent_type` | agent 类型（`"main"` 或 subagent 类型名） |
| `worktree` | agent 运行所在的 git worktree 路径（若有） |
| `effort.level` | （v2.1.133+）当前 effort 级别：`low`/`medium`/`high`/`xhigh`/`max` |

**stdout 结构（退出码 0 才解析）：**

| 字段 | 说明 |
|------|------|
| `continue` | 是否继续 |
| `stopReason` | 停止时的可选消息 |
| `suppressOutput` | 是否抑制输出 |
| `systemMessage` | 系统警告消息 |
| `hookSpecificOutput` | 事件特定输出（如 `permissionDecision`/`updatedInput`/`additionalContext`） |

数据流：stdin JSON → hook → stdout JSON + 退出码，适合可视化。

> [查看 I/O 数据流可视化](assets/hooks-io-flow.html)

## 高频事件

Claude Code 支持共 30 个事件，下表只列最常用的 6 个；其余冷门事件（SubagentStart/Stop、TaskCreated/Completed、Worktree*、Elicitation* 等）延后速查。

| 事件 | 触发时机 | matcher | 能否阻断 | 常见用途 |
|------|----------|---------|----------|----------|
| **PreToolUse** | 工具执行前 | 工具名 | 是（allow/deny/ask） | 校验、修改输入 |
| **PostToolUse** | 工具成功执行后 | 工具名 | 否 | 反馈、添加上下文 |
| **UserPromptSubmit** | 用户提交 prompt | — | 是（block） | 校验 prompt |
| **Stop** | Claude 完成响应 | — | 是 | 任务完成检查 |
| **SessionStart** | 会话开始/恢复/清空/压缩 | startup/resume/clear/compact | 否 | 环境初始化 |
| **SessionEnd** | 会话终止 | — | 否 | 清理、最终日志 |

事件在会话与工具流程中的触发位置（先后顺序、与阻断点的交互）适合可视化。

> [查看事件时序可视化](assets/hooks-event-timeline.html)

## command 类型 + exec args

command hook 有两种执行形式：

**`command` 形式（shell）：** 执行 shell 命令，路径占位符需加引号，支持管道、重定向、`&&` 链和 shell 展开。

```json
{
  "type": "command",
  "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate.py\"",
  "timeout": 60
}
```

**`args` 形式（v2.1.139）：** 通过 `execve()` 直接启动二进制文件，无 shell 解析。路径占位符无需引号，配置不受 shell 注入漏洞影响。

```json
{
  "type": "command",
  "args": ["python3", "$CLAUDE_PROJECT_DIR/.claude/hooks/validate.py", "--strict"],
  "timeout": 60
}
```

两种形式**互斥**——同时设置 `command` 和 `args` 的 hook 会在配置加载时被拒绝。

**决策：** 需要管道、重定向、`&&` 链或 shell 展开时用 `command`；只调用一个带参数的二进制时用 `args`（更安全）。

## 非 command 4 类型

除默认的 `command` 外，还有 4 种 hook 类型：

| 类型 | 机制 | 通信 | 适用场景 | 版本 |
|------|------|------|----------|------|
| **http** | 远程 webhook | 向 URL POST JSON，接收 JSON 响应 | 外部服务、通知 | v2.1.63 |
| **prompt** | LLM 求值 | Claude 求值该 prompt，返回结构化决策 | Stop/SubagentStop 智能完成检查 | — |
| **mcp_tool** | 调用已配置 MCP 工具 | 引用 MCP server + 工具名 | 校验逻辑已存在于某 MCP server | v2.1.118 |
| **agent** | subagent 评估 | 启动专用 agent，可用工具做多步推理 | 复杂架构检查 | — |

每种类型的配置片段：

```json
// http：向 URL POST JSON
{
  "type": "http",
  "url": "https://my-webhook.example.com/hook",
  "matcher": "Write"
}
```

```json
// prompt：LLM 求值
{
  "type": "prompt",
  "prompt": "Evaluate if Claude completed all requested tasks.",
  "timeout": 30
}
```

```json
// mcp_tool：调用已配置的 MCP 工具
{
  "type": "mcp_tool",
  "server": "my-mcp-server",
  "tool": "validate_edit"
}
```

```json
// agent：subagent 评估
{
  "type": "agent",
  "prompt": "Verify the code changes follow our architecture guidelines.",
  "timeout": 120
}
```

**注意：** http hook 的 URL 中如需环境变量插值，必须提供显式的 `allowedEnvVars` 列表。

5 种类型（含 command）并列对比适合可视化。

> [查看类型对比可视化](assets/hooks-type-comparison.html)

## 环境变量

| 变量 | 可用范围 | 说明 |
|------|----------|------|
| `CLAUDE_PROJECT_DIR` | 所有 hook | 项目根目录的绝对路径 |
| `CLAUDE_ENV_FILE` | SessionStart、CwdChanged、FileChanged | 用于持久化环境变量的文件路径 |
| `CLAUDE_CODE_REMOTE` | 所有 hook | 在远程环境中运行时为 `"true"` |
| `${CLAUDE_PLUGIN_ROOT}` | 插件 hook | 插件目录路径 |
| `${CLAUDE_PLUGIN_DATA}` | 插件 hook | 插件数据目录路径 |
| `CLAUDE_CODE_SESSION_ID` | Bash 工具子进程（v2.1.132+） | 会话 UUID；与 hook 输入 JSON 中的 `session_id` 一致 |
| `CLAUDE_EFFORT` | Bash 工具子进程（v2.1.133+） | 当前 effort 级别（`low`/`medium`/`high`/`xhigh`/`max`） |
| `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` | 进程级（v2.1.143+） | 连续 Stop hook 阻断次数上限（默认 `8`，设为 `0` 禁用） |
| `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` | SessionEnd | SessionEnd hook 超时（毫秒） |

## 进阶输出

**`updatedToolOutput`（v2.1.121+）**：`hookSpecificOutput.updatedToolOutput` 对**所有**工具生效（不再仅限 MCP 工具）。针对 `Bash`/`Edit`/`Read` 等的 `PostToolUse` hook 可以在 Claude 看到工具输出前改写它——适用于脱敏、归一化 diff、过滤嘈杂的命令输出。

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "updatedToolOutput": "<plain-text output with ANSI escapes removed>"
  }
}
```

**`terminalSequence`（v2.1.141）**：hook 在 JSON 输出中设置 `terminalSequence` 发送原始 OSC（操作系统命令）转义序列。host 在 hook 返回时把序列写入其控制终端——适用于桌面通知、窗口标题更新、终端响铃，无需自己拥有 TTY。

```json
{
  "terminalSequence": "]9;Task complete"
}
```

把它配置在 `Stop` hook 上，通知会在 Claude 完成一轮时触发。序列支持取决于终端；Kitty/iTerm2/Windows Terminal 支持 OSC 9。

## 可恢复阻断 + Stop 上限

**`continueOnBlock`（v2.1.139）**：默认情况下，返回 `"decision": "block"` 的 `PostToolUse` hook 会中止当前轮次。在该 hook 上设置 `"continueOnBlock": true`，`block` 决策改为把拒绝作为 `tool_result` 返回给 Claude，让模型读到反馈后重试或调整。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/policy-check.py",
            "continueOnBlock": true
          }
        ]
      }
    ]
  }
}
```

当 hook 的 `reason` 是 Claude 能据以行动的内容（如"此文件只读，请写到别处"）时使用它；当阻断必须完全停止本轮时关闭。

**Stop 连续阻断上限（v2.1.143）**：同一轮次连续返回 **8 次** `"decision": "block"`（或 `continue: false`）的 `Stop` hook 会让 Claude Code 短路该循环并警告结束会话。可用环境变量 `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP=<整数>` 覆盖阈值（设为 `0` 完全禁用上限）。防止有 bug 的 Stop hook 让会话无限循环。

## 组件作用域 hooks

skill/agent/command 的 frontmatter 中可直接定义 hooks，把 hook 贴在使用它的组件里，让相关代码放在一起。支持的事件：`PreToolUse`、`PostToolUse`、`Stop`。

```yaml
---
name: secure-operations
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
          once: true
---
```

**Subagent frontmatter 的 Stop 转换**：在 subagent 的 frontmatter 中定义 `Stop` 会**自动转换为**作用于该 subagent 的 `SubagentStop`——只在该 subagent 完成时触发，而非主会话停止时。

hook 贴在组件 + Stop→SubagentStop 转换是空间关系，适合可视化。

> [查看组件作用域可视化](assets/hooks-component-scope.html)

## 安全进阶

- **v2.1.145 bash 裸变量漏洞关闭**：形如 `FOO=bar somecommand` 的 Bash 命令（与非白名单命令内联的裸变量赋值）在 v2.1.145 之前，当只有 `FOO=bar` 本身位于白名单时可能被自动批准；v2.1.145 起触发权限提示。依赖隐式允许的脚本需用覆盖完整命令的 `Bash(...)` 权限规则显式放行，而非仅放行变量赋值。
- **HTTP hook 的 `allowedEnvVars`**：URL 中环境变量插值需提供显式的 `allowedEnvVars` 列表，防止敏感环境变量意外泄露到远程端点。
- **`disableAllHooks` 遵循 managed settings 层级**：组织级设置可强制禁用 hooks，单个用户无法覆盖。
- **工作区信任**：`statusLine` 和 `fileSuggestion` hook 输出命令需先接受工作区信任才会生效。

## 版本演进速查

集中散落各处的版本注，便于跨版本排查。

| 版本 | 变更 |
|------|------|
| v2.1.63 | `http` hook 类型 |
| v2.1.118 | `mcp_tool` hook 类型 |
| v2.1.119 | `PostToolUse`/`PostToolUseFailure` 输入含 `duration_ms`；PowerShell 命令可在权限模式下自动批准 |
| v2.1.121 | `updatedToolOutput` 对所有工具生效（不再仅限 MCP） |
| v2.1.132 | `CLAUDE_CODE_SESSION_ID` 环境变量 |
| v2.1.133 | `CLAUDE_EFFORT` 环境变量 + 输入 `effort.level` |
| v2.1.139 | command 的 `args` 形式（`execve()`）；PostToolUse `continueOnBlock` |
| v2.1.141 | `terminalSequence`（OSC 转义序列） |
| v2.1.143 | Stop hook 连续阻断 8 次上限 |
| v2.1.145 | bash 裸变量自动批准漏洞关闭 |
| v2.1.152 | `MessageDisplay` 事件；SessionStart `reloadSkills`/`sessionTitle` |
| v2.1.153 | statusline 命令收到 `COLUMNS`/`LINES` |
| v2.1.163 | `Stop`/`SubagentStop` 可返回 `hookSpecificOutput.additionalContext` 继续本轮 |

## 三要三不要 + 常见陷阱

| ✅ 要 | ❌ 不要 |
|------|------|
| 校验并清理所有输入 | 盲目信任输入数据 |
| 给 shell 变量加引号 `"$VAR"` | 不加引号 `$VAR` |
| 用 `$CLAUDE_PROJECT_DIR` 绝对路径 | 硬编码路径 |
| 跳过敏感文件（`.env`/`.git`/密钥） | 处理所有文件 |
| 先隔离测试 hook | 部署未测试的 hook |
| HTTP hook 用显式 `allowedEnvVars` | 把所有 env 暴露给 webhook |

**常见陷阱：**

- **hook 不执行** → 核对 JSON 配置语法、matcher 是否匹配工具名、脚本可执行（`chmod +x`）、`claude --debug` 看日志、确认 hook 从 stdin 读 JSON（非命令参数）。
- **hook 意外阻断** → 用示例 JSON 测试 `echo '{...}' | ./hook.py`、查退出码（允许 `0` / 阻断 `2`）、查 stderr。
- **Stop 死循环** → v2.1.143 的 8 次上限保护；用 `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` 调整。
- **JSON 解析错误** → 始终从 stdin 读（非命令参数）、用正确 JSON 解析（非字符串拼接）、优雅处理缺失字段。

## 延后查阅

本文档聚焦二八核心，以下细节速查链回完整教程。

- **24 冷门事件**：SubagentStart/SubagentStop/TaskCreated/TaskCompleted/WorktreeCreate/WorktreeRemove/Elicitation/ElicitationResult/ConfigChange/CwdChanged/FileChanged/PreCompact/PostCompact/Notification/MessageDisplay/StopFailure/TeammateIdle/PermissionRequest/PermissionDenied/PostToolUseFailure/PostToolBatch/Setup/InstructionsLoaded/UserPromptExpansion——见 [zh/06-hooks/README.md#hook-事件](../../zh/06-hooks/README.md#hook-事件)。
- **8 示例**：原文有 validate-bash/security-scan/format-code/validate-prompt/Stop prompt/context-tracker/auto-mode-perms/session-end。本笔记挑 PreToolUse 的 validate-bash 机制（退出码 2 阻断）作为代表已融入正文，其余链回 [zh/06-hooks/README.md#示例](../../zh/06-hooks/README.md#示例)。
- **插件 hooks**：插件在 `hooks/hooks.json` 含 hooks，用 `${CLAUDE_PLUGIN_ROOT}`/`${CLAUDE_PLUGIN_DATA}`——见 [zh/06-hooks/README.md#插件-hooks](../../zh/06-hooks/README.md#插件-hooks)。
- **调试**：`claude --debug` / `Ctrl+O` verbose / `echo '{...}' | ./hook.py` 独立测试——见 [zh/06-hooks/README.md#调试](../../zh/06-hooks/README.md#调试)。
- **安装**：`mkdir -p ~/.claude/hooks` + 复制 + `chmod +x`——见 [zh/06-hooks/README.md#安装](../../zh/06-hooks/README.md#安装)。

## 延伸阅读

- [官方 Hooks 文档](https://code.claude.com/docs/en/hooks)
- [CLI 参考](https://code.claude.com/docs/en/cli-reference)
- [完整教程：zh/06-hooks/README.md](../../zh/06-hooks/README.md)
- 相关模块：[Memory（02-memory）](../../zh/02-memory/README.md)、[Skills（03-skills）](../../zh/03-skills/README.md)、[Subagents（04-subagents）](../../zh/04-subagents/README.md)、[Plugins（07-plugins）](../../zh/07-plugins/README.md)

---

**Last Updated**: 2026 年 6 月 15 日
**Claude Code Version**: 2.1.170
**Sources**:
- https://code.claude.com/docs/en/hooks
- zh/06-hooks/README.md
**Compatible Models**: Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
