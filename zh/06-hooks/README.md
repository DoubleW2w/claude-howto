<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../../resources/logos/claude-howto-logo.svg">
</picture>

# Hooks

Hooks 是在 Claude Code 会话的特定事件触发时自动执行的脚本。它们支持自动化、校验、权限管理和自定义工作流。

## 概览

Hooks 是在 Claude Code 中特定事件发生时自动执行的动作（shell 命令、HTTP webhook、LLM prompt、MCP 工具调用或 subagent 评估）。它们接收 JSON 输入，并通过退出码和 JSON 输出返回结果。

**主要特性：**
- 事件驱动的自动化
- 基于 JSON 的输入/输出
- 支持 `command`、`http`、`mcp_tool`、`prompt` 和 `agent` 五种 hook 类型
- 针对特定工具的模式匹配

## 配置

Hooks 在 settings 文件中按特定结构配置：

- `~/.claude/settings.json` - 用户设置（所有项目）
- `.claude/settings.json` - 项目设置（可共享，提交到 git）
- `.claude/settings.local.json` - 本地项目设置（不提交）
- Managed policy - 组织级设置
- Plugin `hooks/hooks.json` - 插件作用域的 hooks
- Skill/Agent frontmatter - 组件生命周期 hooks

### 基本配置结构

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
|-------|-------------|---------|
| `matcher` | 匹配工具名称的模式（区分大小写） | `"Write"`、`"Edit\|Write"`、`"*"` |
| `hooks` | hook 定义数组 | `[{ "type": "command", ... }]` |
| `type` | Hook 类型：`"command"`（bash）、`"prompt"`（LLM）、`"http"`（webhook）、`"mcp_tool"`（MCP 工具调用，v2.1.118+）或 `"agent"`（subagent） | `"command"` |
| `command` | 要执行的 shell 命令 | `"$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh"` |
| `timeout` | 可选超时时间，单位秒（默认 60） | `30` |
| `once` | 若为 `true`，该 hook 每个会话只运行一次 | `true` |

### Matcher 模式

| 模式 | 说明 | 示例 |
|---------|-------------|---------|
| 精确字符串 | 匹配特定工具 | `"Write"` |
| 正则表达式 | 匹配多个工具 | `"Edit\|Write"` |
| 通配符 | 匹配所有工具 | `"*"` 或 `""` |
| MCP 工具 | server 和工具模式 | `"mcp__memory__.*"` |

**InstructionsLoaded 的 matcher 取值：**

| Matcher 取值 | 说明 |
|---------------|-------------|
| `session_start` | 会话启动时加载指令 |
| `nested_traversal` | 嵌套目录遍历时加载指令 |
| `path_glob_match` | 通过路径 glob 模式匹配加载指令 |

## Hook 类型

Claude Code 支持五种 hook 类型：

### Command Hooks

默认的 hook 类型。执行 shell 命令，通过 JSON stdin/stdout 和退出码通信。

```json
{
  "type": "command",
  "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate.py\"",
  "timeout": 60
}
```

#### exec 形式（`args`）

> v2.1.139 新增。

除 shell 形式的 `"command": "..."` 外，command hook 还可以通过 `args` 数组用 `execve()` 直接启动二进制文件。由于没有 shell 解析，路径占位符无需加引号，配置也不受 shell 注入漏洞影响。

```json
{
  "type": "command",
  "args": ["python3", "$CLAUDE_PROJECT_DIR/.claude/hooks/validate.py", "--strict"],
  "timeout": 60
}
```

两种形式**互斥**——同时设置 `command` 和 `args` 的 hook 会在配置加载时被拒绝。需要管道、重定向、`&&` 链或 shell 展开时用 `command`；只调用一个带参数的二进制时用 `args`。

### HTTP Hooks

> v2.1.63 新增。

远程 webhook 端点，接收和 command hook 相同的 JSON 输入。HTTP hook 向 URL POST JSON 并接收 JSON 响应。启用沙箱时，HTTP hook 会经由沙箱路由。出于安全考虑，URL 中的环境变量插值需要显式的 `allowedEnvVars` 列表。

```json
{
  "hooks": {
    "PostToolUse": [{
      "type": "http",
      "url": "https://my-webhook.example.com/hook",
      "matcher": "Write"
    }]
  }
}
```

**关键属性：**
- `"type": "http"` —— 标识这是一个 HTTP hook
- `"url"` —— webhook 端点 URL
- 启用沙箱时经由沙箱路由
- URL 中如需环境变量插值，必须提供显式的 `allowedEnvVars` 列表

### Prompt Hooks

由 LLM 求值的 prompt——hook 内容是一个由 Claude 求值的 prompt。主要用于 `Stop` 和 `SubagentStop` 事件，做智能的任务完成检查。

```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude completed all requested tasks.",
  "timeout": 30
}
```

LLM 求值该 prompt 并返回结构化决策（详见 [基于 Prompt 的 Hooks](#基于-prompt-的-hooks)）。

### MCP Tool Hooks

> v2.1.118 新增。

`mcp_tool` 类型直接调用已配置的 MCP 工具；配置引用的是 MCP server 和工具名，而非 shell 命令或 URL。当校验或响应逻辑已经存在于你配置的某个 MCP server 时，这很有用。

```json
{
  "matcher": "Edit",
  "hooks": [{
    "type": "mcp_tool",
    "server": "my-mcp-server",
    "tool": "validate_edit"
  }]
}
```

**关键属性：**
- `"type": "mcp_tool"` —— 标识这是一个 MCP 工具 hook
- `"server"` —— 已配置的 MCP server 名称
- `"tool"` —— 该 server 上要调用的工具名

Hook 输入（工具名、工具输入、会话上下文）会作为 MCP 工具的参数传入。MCP server 的配置见 [MCP server 设置](../05-mcp/README.md)。

### Agent Hooks

基于 subagent 的校验 hook，会启动专用 agent 来评估条件或执行复杂检查。和 prompt hook（单轮 LLM 求值）不同，agent hook 可以使用工具并执行多步推理。

```json
{
  "type": "agent",
  "prompt": "Verify the code changes follow our architecture guidelines. Check the relevant design docs and compare.",
  "timeout": 120
}
```

**关键属性：**
- `"type": "agent"` —— 标识这是一个 agent hook
- `"prompt"` —— 给 subagent 的任务描述
- agent 可以使用工具（Read、Grep、Bash 等）执行评估
- 返回和 prompt hook 类似的结构化决策

## Hook 事件

Claude Code 支持 **30 个 hook 事件**：

| 事件 | 触发时机 | Matcher 输入 | 能否阻断 | 常见用途 |
|-------|---------------|---------------|-----------|------------|
| **SessionStart** | 会话开始/恢复/清空/压缩 | startup/resume/clear/compact | 否 | 环境初始化 |
| **Setup** | 初始环境设置（每会话一次） | （无） | 否 | 准备工具、安装依赖 |
| **InstructionsLoaded** | CLAUDE.md 或 rules 文件加载后 | （无） | 否 | 修改/过滤指令 |
| **UserPromptSubmit** | 用户提交 prompt | （无） | 是 | 校验 prompt |
| **UserPromptExpansion** | 用户 prompt 被展开（如 `@` 提及、slash command 解析） | （无） | 是 | 转换或检查展开后的 prompt |
| **PreToolUse** | 工具执行前 | 工具名 | 是（allow/deny/ask） | 校验、修改输入 |
| **PermissionRequest** | 权限对话框出现 | 工具名 | 是 | 自动批准/拒绝 |
| **PermissionDenied** | 用户拒绝权限提示 | 工具名 | 否 | 日志、分析、策略执行 |
| **PostToolUse** | 工具成功执行后 | 工具名 | 否 | 添加上下文、反馈 |
| **PostToolUseFailure** | 工具执行失败 | 工具名 | 否 | 错误处理、日志 |
| **PostToolBatch** | 一批工具调用完成后 | （无） | 否 | 汇总报告、批量校验 |
| **Notification** | 发送通知 | 通知类型 | 否 | 自定义通知 |
| **MessageDisplay** | 助手消息文本展示时 | （无） | 否 | 转换或隐藏展示的消息文本（v2.1.152） |
| **SubagentStart** | subagent 启动 | agent 类型名 | 否 | subagent 初始化 |
| **SubagentStop** | subagent 结束 | agent 类型名 | 是 | subagent 校验 |
| **Stop** | Claude 完成响应 | （无） | 是 | 任务完成检查 |
| **StopFailure** | API 错误结束本轮 | （无） | 否 | 错误恢复、日志 |
| **TeammateIdle** | agent 团队成员空闲 | （无） | 是 | 团队成员协调 |
| **TaskCompleted** | 任务标记为完成 | （无） | 是 | 任务后动作 |
| **TaskCreated** | 通过 TaskCreate 创建任务 | （无） | 否 | 任务跟踪、日志 |
| **ConfigChange** | 配置文件变化 | （无） | 是（policy 除外） | 响应配置更新 |
| **CwdChanged** | 工作目录变化 | （无） | 否 | 目录相关初始化 |
| **FileChanged** | 监视的文件变化 | （无） | 否 | 文件监视、重建 |
| **PreCompact** | 上下文压缩前 | manual/auto | 否 | 压缩前动作 |
| **PostCompact** | 压缩完成后 | （无） | 否 | 压缩后动作 |
| **WorktreeCreate** | 创建 worktree | （无） | 是（返回路径） | worktree 初始化 |
| **WorktreeRemove** | 移除 worktree | （无） | 否 | worktree 清理 |
| **Elicitation** | MCP server 请求用户输入 | （无） | 是 | 输入校验 |
| **ElicitationResult** | 用户响应 elicitation | （无） | 是 | 响应处理 |
| **SessionEnd** | 会话终止 | （无） | 否 | 清理、最终日志 |

> **PostToolUse 时长（v2.1.119）：** `PostToolUse` 和 `PostToolUseFailure` hook 的输入现在包含 `duration_ms`——详见 [PostToolUse](#posttooluse) 章节。

### PreToolUse

在 Claude 创建工具参数之后、处理之前运行。用于校验或修改工具输入。

**配置：**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py"
          }
        ]
      }
    ]
  }
}
```

**常见 matcher：** `Task`、`Bash`、`Glob`、`Grep`、`Read`、`Edit`、`Write`、`WebFetch`、`WebSearch`

**输出控制：**
- `permissionDecision`：`"allow"`、`"deny"` 或 `"ask"`
- `permissionDecisionReason`：决策理由
- `updatedInput`：修改后的工具输入参数

### PostToolUse

工具完成后立即运行。用于校验、日志或向 Claude 提供上下文。

**配置：**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/security-scan.py"
          }
        ]
      }
    ]
  }
}
```

**输出控制：**
- `"block"` 决策会向 Claude 反馈
- `additionalContext`：为 Claude 添加的上下文

**额外输入字段（v2.1.119）：**

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `duration_ms` | number | 工具执行耗时（毫秒）。不包括权限提示和 PreToolUse hook 执行所花时间。`PostToolUse` 和 `PostToolUseFailure` hook 均可用。 |

#### 可恢复阻断（`continueOnBlock`，v2.1.139）

默认情况下，返回 `"decision": "block"` 的 `PostToolUse` hook 会中止当前轮次。在该 hook 上设置 `"continueOnBlock": true`，可改为把拒绝作为 `tool_result` 返回给 Claude，让模型读到反馈后重试或调整。

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

当 hook 的 `reason` 是 Claude 能据以行动的内容时（例如"此文件只读，请写到别处"）使用它；当阻断必须完全停止本轮时则关闭。

### UserPromptSubmit

用户提交 prompt 时、Claude 处理之前运行。

**配置：**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-prompt.py"
          }
        ]
      }
    ]
  }
}
```

**输出控制：**
- `decision`：`"block"` 阻止处理
- `reason`：阻断时的说明
- `additionalContext`：添加到 prompt 的上下文

### Stop 和 SubagentStop

在 Claude 完成响应（Stop）或 subagent 完成（SubagentStop）时运行。支持基于 prompt 的智能任务完成检查。

**额外输入字段：** `Stop` 和 `SubagentStop` hook 的 JSON 输入都包含 `last_assistant_message` 字段，即停止前 Claude 或 subagent 的最后一条消息。这对评估任务完成很有用。

**配置：**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude completed all requested tasks.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

> **连续阻断安全上限（v2.1.143）**：如果 `Stop` hook 对同一轮次连续返回 **8 次** `"decision": "block"`（或设置 `continue: false`），Claude Code 会短路该循环并警告结束会话。可用环境变量 `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP=<整数>` 覆盖阈值（设为 `0` 完全禁用上限）。防止有 bug 的 Stop hook 让会话无限循环。

**返回字段（v2.1.163）：** `Stop` 或 `SubagentStop` hook 可以返回 `hookSpecificOutput.additionalContext` 向 Claude 提供反馈，并**在不抛出错误标签的情况下继续本轮**。以前从 Stop hook 影响模型很别扭；现在 hook 可以干净地注入上下文，避免旧反馈路径（如 `"decision": "block"`）的错误标签行为。

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "additionalContext": "Reminder: run the test suite before declaring done."
  }
}
```

### SubagentStart

subagent 开始执行时运行。matcher 输入是 agent 类型名，让 hook 能针对特定 subagent 类型。

**配置：**
```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "code-review",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/subagent-init.sh"
          }
        ]
      }
    ]
  }
}
```

### SessionStart

会话开始或恢复时运行。可持久化环境变量。

**Matcher：** `startup`、`resume`、`clear`、`compact`

**特殊能力：** 用 `CLAUDE_ENV_FILE` 持久化环境变量（`CwdChanged` 和 `FileChanged` hook 中也可用）：

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

**会话作用域输出（v2.1.152）：** `SessionStart` hook 可以返回 JSON 来重新扫描 skills 并设置会话标题：

```json
{
  "reloadSkills": true,
  "hookSpecificOutput": {
    "sessionTitle": "Payments migration"
  }
}
```

顶层的 `reloadSkills: true` 会在当前会话触发 skill 重新扫描（与 `/reload-skills` 命令相同），让该 hook 刚安装的 skill 立即可用。`hookSpecificOutput.sessionTitle` 在启动和恢复时设置会话的显示标题。

### SessionEnd

会话结束时运行，做清理或最终日志。不能阻断终止。

**reason 字段取值：**
- `clear` - 用户清空了会话
- `logout` - 用户登出
- `prompt_input_exit` - 用户通过 prompt 输入退出
- `other` - 其他原因

**配置：**
```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-cleanup.sh\""
          }
        ]
      }
    ]
  }
}
```

### Notification 事件

通知事件更新后的 matcher：
- `permission_prompt` - 权限请求通知
- `idle_prompt` - 空闲状态通知
- `auth_success` - 认证成功
- `elicitation_dialog` - 向用户展示的对话框

## 组件作用域 Hooks

Hooks 可以附加到特定组件（skills、agents、commands）的 frontmatter 中：

**在 SKILL.md、agent.md 或 command.md 中：**

```yaml
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
          once: true  # 每个会话只运行一次
---
```

**组件 hook 支持的事件：** `PreToolUse`、`PostToolUse`、`Stop`

这样可以把 hook 直接定义在使用它的组件里，让相关代码放在一起。

### Subagent Frontmatter 中的 Hooks

当在 subagent 的 frontmatter 中定义 `Stop` hook 时，它会自动转换为作用于该 subagent 的 `SubagentStop` hook。这确保 stop hook 只在该 subagent 完成时触发，而非主会话停止时。

```yaml
---
name: code-review-agent
description: Automated code review subagent
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: "Verify the code review is thorough and complete."
  # 上面的 Stop hook 会自动转换为该 subagent 的 SubagentStop
---
```

## PermissionRequest 事件

用自定义输出格式处理权限请求：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": {},
      "message": "Custom message",
      "interrupt": false
    }
  }
}
```

## Hook 输入与输出

### JSON 输入（通过 stdin）

所有 hook 通过 stdin 接收 JSON 输入：

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.js",
    "content": "..."
  },
  "tool_use_id": "toolu_01ABC123...",
  "agent_id": "agent-abc123",
  "agent_type": "main",
  "worktree": "/path/to/worktree",
  "effort": { "level": "medium" }
}
```

**常见字段：**

| 字段 | 说明 |
|-------|-------------|
| `session_id` | 唯一会话标识符 |
| `transcript_path` | 对话记录文件路径 |
| `cwd` | 当前工作目录 |
| `hook_event_name` | 触发该 hook 的事件名 |
| `agent_id` | 运行该 hook 的 agent 标识符 |
| `agent_type` | agent 类型（`"main"`、subagent 类型名等） |
| `worktree` | agent 运行所在的 git worktree 路径（若有） |
| `effort.level` | （v2.1.133+）当前 effort 级别：`low`、`medium`、`high`、`xhigh` 或 `max` |

### 退出码

| 退出码 | 含义 | 行为 |
|-----------|---------|----------|
| **0** | 成功 | 继续，解析 JSON stdout |
| **2** | 阻断性错误 | 阻断操作，stderr 作为错误展示 |
| **其他** | 非阻断性错误 | 继续，stderr 在 verbose 模式展示 |

### JSON 输出（stdout，退出码 0）

```json
{
  "continue": true,
  "stopReason": "Optional message if stopping",
  "suppressOutput": false,
  "systemMessage": "Optional warning message",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "File is in allowed directory",
    "updatedInput": {
      "file_path": "/modified/path.js"
    }
  }
}
```

> **作用范围（v2.1.121+）：** `hookSpecificOutput.updatedToolOutput` 现在对**所有**工具生效，不再仅限 MCP 工具。针对 `Bash`、`Edit`、`Read` 等的 `PostToolUse` hook 可以在 Claude 看到工具输出前改写它——适用于脱敏、归一化 diff 或过滤嘈杂的命令输出。示例（从 `Bash` 输出中剥离 ANSI 颜色码）：
>
> ```json
> {
>   "hookSpecificOutput": {
>     "hookEventName": "PostToolUse",
>     "updatedToolOutput": "<plain-text output with ANSI escapes removed>"
>   }
> }
> ```

#### `terminalSequence`（v2.1.141）

Hook 可以在 JSON 输出中设置 `terminalSequence` 来发送原始 OSC（操作系统命令）转义序列。host 在 hook 返回时把序列写入其控制终端——适用于桌面通知、窗口标题更新和终端响铃，无需自己拥有 TTY。

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `terminalSequence` | string | 原始转义序列（通常是 OSC 9 / OSC 0 / OSC 777）。逐字写入 host 终端。 |

示例——长任务完成时触发 OSC 9 桌面通知：

```json
{
  "terminalSequence": "]9;Task complete"
}
```

把它配置在 `Stop` hook 上，通知会在 Claude 完成一轮时触发。序列支持取决于终端；Kitty/iTerm2/Windows Terminal 支持 OSC 9。

## 环境变量

| 变量 | 可用范围 | 说明 |
|----------|-------------|-------------|
| `CLAUDE_PROJECT_DIR` | 所有 hook | 项目根目录的绝对路径 |
| `CLAUDE_ENV_FILE` | SessionStart、CwdChanged、FileChanged | 用于持久化环境变量的文件路径 |
| `CLAUDE_CODE_REMOTE` | 所有 hook | 在远程环境中运行时为 `"true"` |
| `${CLAUDE_PLUGIN_ROOT}` | 插件 hook | 插件目录路径 |
| `${CLAUDE_PLUGIN_DATA}` | 插件 hook | 插件数据目录路径 |
| `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` | SessionEnd hook | SessionEnd hook 的可配置超时（毫秒，覆盖默认值） |
| `CLAUDE_CODE_SESSION_ID` | Bash 工具子进程（v2.1.132+） | 会话 UUID；与 hook 输入 JSON 中的 `session_id` 一致。用于把 bash 日志与 hook 遥测关联。 |
| `CLAUDE_EFFORT` | Bash 工具子进程（v2.1.133+） | 当前 effort 级别（`low`/`medium`/`high`/`xhigh`/`max`）；与 hook 输入 JSON 中的 `effort.level` 一致。 |
| `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` | 进程级（v2.1.143+） | 会话因警告结束前允许的连续 Stop hook 阻断次数（默认 `8`）。设为 `0` 禁用上限。 |

## 基于 Prompt 的 Hooks

对 `Stop` 和 `SubagentStop` 事件，可以使用基于 LLM 的求值：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review if all tasks are complete. Return your decision.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**LLM 响应 schema：**
```json
{
  "decision": "approve",
  "reason": "All tasks completed successfully",
  "continue": false,
  "stopReason": "Task complete"
}
```

## 示例

### 示例 1：Bash 命令校验器（PreToolUse）

**文件：** `.claude/hooks/validate-bash.py`

```python
#!/usr/bin/env python3
import json
import sys
import re

BLOCKED_PATTERNS = [
    (r"\brm\s+-rf\s+/", "Blocking dangerous rm -rf / command"),
    (r"\bsudo\s+rm", "Blocking sudo rm command"),
]

def main():
    input_data = json.load(sys.stdin)

    tool_name = input_data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    command = input_data.get("tool_input", {}).get("command", "")

    for pattern, message in BLOCKED_PATTERNS:
        if re.search(pattern, command):
            print(message, file=sys.stderr)
            sys.exit(2)  # 退出码 2 = 阻断性错误

    sys.exit(0)

if __name__ == "__main__":
    main()
```

**配置：**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py\""
          }
        ]
      }
    ]
  }
}
```

### 示例 2：安全扫描器（PostToolUse）

**文件：** `.claude/hooks/security-scan.py`

```python
#!/usr/bin/env python3
import json
import sys
import re

SECRET_PATTERNS = [
    (r"password\s*=\s*['\"][^'\"]+['\"]", "Potential hardcoded password"),
    (r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]", "Potential hardcoded API key"),
]

def main():
    input_data = json.load(sys.stdin)

    tool_name = input_data.get("tool_name", "")
    if tool_name not in ["Write", "Edit"]:
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    content = tool_input.get("content", "") or tool_input.get("new_string", "")
    file_path = tool_input.get("file_path", "")

    warnings = []
    for pattern, message in SECRET_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            warnings.append(message)

    if warnings:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": f"Security warnings for {file_path}: " + "; ".join(warnings)
            }
        }
        print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 示例 3：自动格式化代码（PostToolUse）

**文件：** `.claude/hooks/format-code.sh`

```bash
#!/bin/bash

# 从 stdin 读取 JSON
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_name', ''))")
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_input', {}).get('file_path', ''))")

if [ "$TOOL_NAME" != "Write" ] && [ "$TOOL_NAME" != "Edit" ]; then
    exit 0
fi

# 按文件扩展名格式化
case "$FILE_PATH" in
    *.js|*.jsx|*.ts|*.tsx|*.json)
        command -v prettier &>/dev/null && prettier --write "$FILE_PATH" 2>/dev/null
        ;;
    *.py)
        command -v black &>/dev/null && black "$FILE_PATH" 2>/dev/null
        ;;
    *.go)
        command -v gofmt &>/dev/null && gofmt -w "$FILE_PATH" 2>/dev/null
        ;;
esac

exit 0
```

### 示例 4：Prompt 校验器（UserPromptSubmit）

**文件：** `.claude/hooks/validate-prompt.py`

```python
#!/usr/bin/env python3
import json
import sys
import re

BLOCKED_PATTERNS = [
    (r"delete\s+(all\s+)?database", "Dangerous: database deletion"),
    (r"rm\s+-rf\s+/", "Dangerous: root deletion"),
]

def main():
    input_data = json.load(sys.stdin)
    prompt = input_data.get("user_prompt", "") or input_data.get("prompt", "")

    for pattern, message in BLOCKED_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            output = {
                "decision": "block",
                "reason": f"Blocked: {message}"
            }
            print(json.dumps(output))
            sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 示例 5：智能 Stop Hook（基于 Prompt）

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review if Claude completed all requested tasks. Check: 1) Were all files created/modified? 2) Were there unresolved errors? If incomplete, explain what's missing.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 示例 6：上下文用量追踪器（Hook 配对）

用 `UserPromptSubmit`（消息前）和 `Stop`（响应后）hook 配合，按请求追踪 token 消耗。

**文件：** `.claude/hooks/context-tracker.py`

```python
#!/usr/bin/env python3
"""
上下文用量追踪器 - 按请求追踪 token 消耗。

用 UserPromptSubmit 作为“消息前”hook、Stop 作为“响应后”hook，
计算每次请求的 token 用量差值。

Token 计数方式：
1. 字符估算（默认）：约 4 字符/token，无依赖
2. tiktoken（可选）：更准确（约 90-95%），需要：pip install tiktoken
"""
import json
import os
import sys
import tempfile

# 配置
CONTEXT_LIMIT = 128000  # Claude 的上下文窗口（按你的模型调整）
USE_TIKTOKEN = False    # 若已安装 tiktoken 以获得更好准确度，设为 True


def get_state_file(session_id: str) -> str:
    """获取存储消息前 token 数的临时文件路径，按会话隔离。"""
    return os.path.join(tempfile.gettempdir(), f"claude-context-{session_id}.json")


def count_tokens(text: str) -> int:
    """
    统计文本中的 token 数。

    若可用则使用 tiktoken 的 p50k_base 编码（约 90-95% 准确度），
    否则回退到字符估算（约 80-90% 准确度）。
    """
    if USE_TIKTOKEN:
        try:
            import tiktoken
            enc = tiktoken.get_encoding("p50k_base")
            return len(enc.encode(text))
        except ImportError:
            pass  # 回退到估算

    # 基于字符的估算：英文约 4 字符/token
    return len(text) // 4


def read_transcript(transcript_path: str) -> str:
    """读取并拼接记录文件中的所有内容。"""
    if not transcript_path or not os.path.exists(transcript_path):
        return ""

    content = []
    with open(transcript_path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                # 从各种消息格式中提取文本内容
                if "message" in entry:
                    msg = entry["message"]
                    if isinstance(msg.get("content"), str):
                        content.append(msg["content"])
                    elif isinstance(msg.get("content"), list):
                        for block in msg["content"]:
                            if isinstance(block, dict) and block.get("type") == "text":
                                content.append(block.get("text", ""))
            except json.JSONDecodeError:
                continue

    return "\n".join(content)


def handle_user_prompt_submit(data: dict) -> None:
    """消息前 hook：保存请求前的当前 token 数。"""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens(transcript_content)

    # 保存到临时文件供后续比较
    state_file = get_state_file(session_id)
    with open(state_file, "w") as f:
        json.dump({"pre_tokens": current_tokens}, f)


def handle_stop(data: dict) -> None:
    """响应后 hook：计算并报告 token 差值。"""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens(transcript_content)

    # 读取消息前的计数
    state_file = get_state_file(session_id)
    pre_tokens = 0
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                state = json.load(f)
                pre_tokens = state.get("pre_tokens", 0)
        except (json.JSONDecodeError, IOError):
            pass

    # 计算差值
    delta_tokens = current_tokens - pre_tokens
    remaining = CONTEXT_LIMIT - current_tokens
    percentage = (current_tokens / CONTEXT_LIMIT) * 100

    # 报告用量
    method = "tiktoken" if USE_TIKTOKEN else "estimated"
    print(f"Context ({method}): ~{current_tokens:,} tokens ({percentage:.1f}% used, ~{remaining:,} remaining)", file=sys.stderr)
    if delta_tokens > 0:
        print(f"This request: ~{delta_tokens:,} tokens", file=sys.stderr)


def main():
    data = json.load(sys.stdin)
    event = data.get("hook_event_name", "")

    if event == "UserPromptSubmit":
        handle_user_prompt_submit(data)
    elif event == "Stop":
        handle_stop(data)

    sys.exit(0)


if __name__ == "__main__":
    main()
```

**配置：**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/context-tracker.py\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/context-tracker.py\""
          }
        ]
      }
    ]
  }
}
```

**工作原理：**
1. `UserPromptSubmit` 在你的 prompt 被处理前触发——保存当前 token 数
2. `Stop` 在 Claude 响应后触发——计算差值并报告用量
3. 每个会话通过临时文件名中的 `session_id` 隔离

**Token 计数方式：**

| 方式 | 准确度 | 依赖 | 速度 |
|--------|----------|--------------|-------|
| 字符估算 | ~80-90% | 无 | <1ms |
| tiktoken（p50k_base） | ~90-95% | `pip install tiktoken` | <10ms |

> **注意：** Anthropic 尚未发布官方离线 tokenizer。两种方式都是近似。记录文件包含用户 prompt、Claude 的响应和工具输出，但不包含系统 prompt 或内部上下文。

### 示例 7：填充 Auto-Mode 权限（一次性设置脚本）

一个一次性设置脚本，向 `~/.claude/settings.json` 填入约 67 条等价于 Claude Code auto-mode 基线的安全权限规则——无需任何 hook，也无需记忆未来的选择。运行一次即可；可安全重复运行（跳过已存在的规则）。

**文件：** `09-advanced-features/setup-auto-mode-permissions.py`

```bash
# 预览将要添加的内容
python3 09-advanced-features/setup-auto-mode-permissions.py --dry-run

# 应用
python3 09-advanced-features/setup-auto-mode-permissions.py
```

**会添加的内容：**

| 类别 | 示例 |
|----------|---------|
| 内置工具 | `Read(*)`、`Edit(*)`、`Write(*)`、`Glob(*)`、`Grep(*)`、`Agent(*)`、`WebSearch(*)` |
| Git 只读 | `Bash(git status:*)`、`Bash(git log:*)`、`Bash(git diff:*)` |
| Git 写入（本地） | `Bash(git add:*)`、`Bash(git commit:*)`、`Bash(git checkout:*)` |
| 包管理器 | `Bash(npm install:*)`、`Bash(pip install:*)`、`Bash(cargo build:*)` |
| 构建与测试 | `Bash(make:*)`、`Bash(pytest:*)`、`Bash(go test:*)` |
| 常用 shell | `Bash(ls:*)`、`Bash(cat:*)`、`Bash(find:*)`、`Bash(cp:*)`、`Bash(mv:*)` |
| GitHub CLI | `Bash(gh pr view:*)`、`Bash(gh pr create:*)`、`Bash(gh issue list:*)` |

**刻意排除的内容**（本脚本永不添加）：
- `rm -rf`、`sudo`、force push、`git reset --hard`
- `DROP TABLE`、`kubectl delete`、`terraform destroy`
- `npm publish`、`curl | bash`、生产部署

### 示例 8：学习进度记录器（SessionEnd）

在每个 Claude Code 会话结束时记录你学了哪些模块。进度存储在 `~/.claude-howto-progress.json`——在仓库之外，所以 `git pull` 不会被覆盖。

**为什么用 `SessionEnd` 而非 `Stop`？**
`Stop` 在 Claude *每次*响应后触发。`SessionEnd` 在会话终止时触发一次——正是一个会话结束日记所需要的。

**为什么用 `/dev/tty` 读取输入？**
Hook 脚本通过 `stdin` 接收 hook JSON 负载，所以交互式 `read` 必须直接用 `/dev/tty` 才能到达终端。

**文件：** `06-hooks/session-end.sh`

```bash
#!/usr/bin/env bash
# SessionEnd hook：询问学习了哪些模块，然后把一条会话记录追加到
# ~/.claude-howto-progress.json，用于持久化学习进度跟踪。

PROGRESS_FILE="$HOME/.claude-howto-progress.json"

# 守卫：仅在本仓库内运行
if [[ "$CLAUDE_PROJECT_DIR" != *"claude-howto"* ]] && [[ "$PWD" != *"claude-howto"* ]]; then
  exit 0
fi

if [ ! -f "$PROGRESS_FILE" ]; then
  echo '{"sessions":[]}' > "$PROGRESS_FILE"
fi

DATE=$(date +"%Y-%m-%d")
TIME=$(date +"%H:%M")

echo ""
echo " 你学习了哪些模块？（例如 06,07 或回车跳过）"
echo " 01=Slash  02=Memory  03=Skills  04=Subagents  05=MCP"
echo " 06=Hooks  07=Plugins 08=Checkpoints 09=Advanced 10=CLI"
printf " > "
read -r INPUT </dev/tty

if [ -z "$INPUT" ] || [ "$INPUT" = "skip" ]; then
  exit 0
fi

MODULES_JSON=$(echo "$INPUT" | tr ',' '\n' | tr -d ' ' | while read -r m; do
  case "$m" in
    01) echo '"01-slash-commands"' ;;
    02) echo '"02-memory"' ;;
    03) echo '"03-skills"' ;;
    04) echo '"04-subagents"' ;;
    05) echo '"05-mcp"' ;;
    06) echo '"06-hooks"' ;;
    07) echo '"07-plugins"' ;;
    08) echo '"08-checkpoints"' ;;
    09) echo '"09-advanced-features"' ;;
    10) echo '"10-cli"' ;;
    *)  echo "\"$m\"" ;;
  esac
done | paste -sd ',' -)

printf " 备注？（可选，回车跳过）："
read -r NOTES </dev/tty

# 把 NOTES 作为单独参数传入，让 Python 处理 JSON 转义——
# 避免备注中含引号或反斜杠时生成损坏的 JSON。
python3 - "$PROGRESS_FILE" "$DATE" "$TIME" "$MODULES_JSON" "$NOTES" <<'PYEOF'
import sys, json

path, date, time_str, modules_raw, notes = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]

new_session = {
    "date": date,
    "time": time_str,
    "modules": json.loads(f"[{modules_raw}]") if modules_raw else [],
    "notes": notes,
}

with open(path, 'r') as f:
    data = json.load(f)

data.setdefault('sessions', []).append(new_session)

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
PYEOF

echo " 已保存到 $PROGRESS_FILE"
```

**安装**——把脚本复制到项目的 hook 目录，让 `settings.json` 中的路径能解析到：

```bash
mkdir -p .claude/hooks
cp 06-hooks/session-end.sh .claude/hooks/
chmod +x .claude/hooks/session-end.sh
```

**配置**（在 `.claude/settings.json` 中）：

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-end.sh\""
          }
        ]
      }
    ]
  }
}
```

**输出 —— `~/.claude-howto-progress.json`：**

```json
{
  "sessions": [
    {
      "date": "2026-04-18",
      "time": "14:32",
      "modules": ["06-hooks", "07-plugins"],
      "notes": "Installed first hook, tried pre-commit example"
    }
  ]
}
```

**展示的关键模式：**

| 模式 | 为何重要 |
|---------|----------------|
| `SessionEnd` 事件 | 退出时触发一次——不像 `Stop` 那样每次响应后都触发 |
| `read -r INPUT </dev/tty` | Hook 占用 `stdin`（JSON 负载）；用户输入要用 `/dev/tty` |
| `$CLAUDE_PROJECT_DIR` | 可移植路径——切勿硬编码 `/Users/yourname/...` |
| 顶部守卫子句 | 若全局安装，防止 hook 在无关项目里运行 |
| 存到仓库外 | `~/` 路径能扛住 `git pull`，不会被覆盖 |

**配套：可视化进度追踪器**

若要覆盖全部 10 个模块的完整勾选 UI，在浏览器中打开内置追踪器：

```bash
open local-progress/index.html
```

进度存在浏览器 `localStorage`（绝不写进仓库磁盘）。用 **Export** 按钮把快照存为 JSON，用 **Import** 恢复。

## 插件 Hooks

插件可以在 `hooks/hooks.json` 文件中包含 hooks：

**文件：** `plugins/hooks/hooks.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  }
}
```

**插件 Hook 中的环境变量：**
- `${CLAUDE_PLUGIN_ROOT}` - 插件目录路径
- `${CLAUDE_PLUGIN_DATA}` - 插件数据目录路径

这让插件可以包含自定义校验和自动化 hooks。

## MCP Tool Hooks

MCP 工具遵循 `mcp__<server>__<tool>` 模式：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"systemMessage\": \"Memory operation logged\"}'"
          }
        ]
      }
    ]
  }
}
```

## 安全注意事项

### 免责声明

**风险自负**：Hooks 会执行任意 shell 命令。你需对以下事项负全责：
- 你配置的命令
- 文件访问/修改权限
- 潜在的数据丢失或系统损坏
- 生产使用前在安全环境中测试 hooks

### 安全说明

- **需要工作区信任：** `statusLine` 和 `fileSuggestion` hook 输出命令现在需要先接受工作区信任才会生效。
- **Status-line 终端尺寸（v2.1.153）：** Status-line 命令脚本现在会收到 `COLUMNS` 和 `LINES` 环境变量，脚本可以据此调整输出以适配终端宽/高（例如 `[ "$COLUMNS" -lt 80 ] && short_output`）。
- **HTTP hook 与环境变量：** HTTP hook 需要显式的 `allowedEnvVars` 列表才能在 URL 中使用环境变量插值。防止敏感环境变量意外泄露到远程端点。
- **Managed settings 层级：** `disableAllHooks` 设置现在遵循 managed settings 层级，意味着组织级设置可以强制禁用 hooks，单个用户无法覆盖。
- **PowerShell 自动批准（v2.1.119）：** PowerShell 工具命令现在可以在权限模式下自动批准，与 Bash 对齐。这让用 PowerShell 作为 shell 工具的 Windows 用户获得对等体验。
- **Bash 裸环境变量自动批准漏洞关闭（v2.1.145）：** v2.1.145 之前，形如 `FOO=bar somecommand` 的 Bash 命令（与非白名单命令内联的裸变量赋值）在只有 `FOO=bar` 本身位于白名单时可能被自动批准。v2.1.145 关闭了这一点——这类命令现在会触发权限提示。依赖隐式允许的脚本会开始提示；请通过覆盖完整命令的 `Bash(...)` 权限规则显式重新放行，而非仅放行变量赋值。

### 最佳实践

| 该做 | 不该做 |
|-----|-------|
| 校验并清理所有输入 | 盲目信任输入数据 |
| 给 shell 变量加引号：`"$VAR"` | 不加引号：`$VAR` |
| 阻断路径穿越（`..`） | 允许任意路径 |
| 用 `$CLAUDE_PROJECT_DIR` 的绝对路径 | 硬编码路径 |
| 跳过敏感文件（`.env`、`.git/`、密钥） | 处理所有文件 |
| 先隔离测试 hook | 部署未测试的 hook |
| HTTP hook 用显式 `allowedEnvVars` | 把所有环境变量暴露给 webhook |

## 调试

### 启用调试模式

带 debug 标志运行 Claude 以获取详细 hook 日志：

```bash
claude --debug
```

### Verbose 模式

在 Claude Code 中按 `Ctrl+O` 启用 verbose 模式，查看 hook 执行进度。

### 独立测试 Hook

```bash
# 用示例 JSON 输入测试
echo '{"tool_name": "Bash", "tool_input": {"command": "ls -la"}}' | python3 .claude/hooks/validate-bash.py

# 查看退出码
echo $?
```

## 完整配置示例

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py\"",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/format-code.sh\"",
            "timeout": 30
          },
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/security-scan.py\"",
            "timeout": 10
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-prompt.py\""
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-init.sh\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verify all tasks are complete before stopping.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Hook 执行细节

| 方面 | 行为 |
|--------|----------|
| **超时** | 默认 60 秒，可按命令配置 |
| **并行化** | 所有匹配的 hook 并行运行 |
| **去重** | 相同的 hook 命令会去重 |
| **环境** | 在当前目录、Claude Code 的环境中运行 |

## 故障排查

### Hook 不执行
- 核对 JSON 配置语法正确
- 检查 matcher 模式是否匹配工具名
- 确保脚本存在且可执行：`chmod +x script.sh`
- 运行 `claude --debug` 查看 hook 执行日志
- 确认 hook 从 stdin 读取 JSON（而非命令参数）

### Hook 意外阻断
- 用示例 JSON 测试 hook：`echo '{"tool_name": "Write", ...}' | ./hook.py`
- 检查退出码：允许应为 0，阻断应为 2
- 检查 stderr 输出（退出码 2 时展示）

### JSON 解析错误
- 始终从 stdin 读取，而非命令参数
- 用正确的 JSON 解析（而非字符串拼接）
- 优雅处理缺失字段

## 安装

### 第 1 步：创建 Hooks 目录
```bash
mkdir -p ~/.claude/hooks
```

### 第 2 步：复制示例 Hooks
```bash
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

### 第 3 步：在 Settings 中配置
用上文展示的 hook 配置编辑 `~/.claude/settings.json` 或 `.claude/settings.json`。

## 相关概念

- **[Checkpoints 和 Rewind](../08-checkpoints/)** - 保存和恢复会话状态
- **[Slash Commands](../01-slash-commands/)** - 创建自定义 slash command
- **[Skills](../03-skills/)** - 可复用的自主能力
- **[Subagents](../04-subagents/)** - 委派的任务执行
- **[Plugins](../07-plugins/)** - 打包的扩展包
- **[高级功能](../09-advanced-features/)** - 探索 Claude Code 高级能力

## 更多资源

- **[官方 Hooks 文档](https://code.claude.com/docs/en/hooks)** - 完整 hooks 参考
- **[CLI 参考](https://code.claude.com/docs/en/cli-reference)** - 命令行界面文档
- **[Memory 指南](../02-memory/)** - 持久上下文配置

---

**最后更新**：2026 年 6 月 10 日
**Claude Code 版本**：2.1.170
**来源**：
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/changelog
- https://github.com/anthropics/claude-code/releases/tag/v2.1.139
- https://github.com/anthropics/claude-code/releases/tag/v2.1.145
- https://github.com/anthropics/claude-code/releases/tag/v2.1.152
- https://github.com/anthropics/claude-code/releases/tag/v2.1.153
**兼容模型**：Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
