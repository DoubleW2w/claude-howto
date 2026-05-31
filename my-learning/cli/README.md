# CLI 核心知识

> 用[二八法则学习方法论](../learning-methodology/README.md)从 `zh/10-cli/README.md`（964行）提炼的 20% 核心知识。详细内容见 [10-cli 完整教程](../../zh/10-cli/README.md)。
>
> **可视化决策**：✅ 生成 4 个 HTML。理由：两种运行模式（概念易混淆对比）、权限模式（分支决策）、会话管理（状态轮转）、打印三板斧（场景演示）。纯命令/标志/文本部分不生成。

## 一句话定义

`claude` 命令是与 Claude Code 交互的唯一入口——启动会话、查询、管理模型、控制权限，全从这里开始。

## 核心命令（5个）

| 命令 | 做什么 | 示例 |
|------|--------|------|
| `claude` | 启动交互式 REPL | `claude` |
| `claude -p "query"` | 提问后退出（脚本友好） | `claude -p "explain this function"` |
| `claude -c` | 继续最近一次会话 | `claude -c` |
| `claude -r "name"` | 按名称恢复会话 | `claude -r "auth-refactor"` |
| `claude update` | 更新版本 | `claude update` |

## 两种运行模式

这是 CLI 最重要的架构概念——决定了 Claude 怎么输出、你能做什么：

| 模式 | 命令 | 特点 | 适用场景 |
|------|------|------|---------|
| **交互式 REPL** | `claude` | 多轮对话、Tab补全、slash命令 | 日常开发、探索性工作 |
| **打印模式** | `claude -p` | 单次查询、可脚本化、可管道、JSON输出 | CI/CD、脚本、管道串联 |

> [查看交互式对比演示](assets/cli-modes-compare.html)

```bash
# 交互模式
claude "explain the auth flow"

# 打印模式
claude -p "what does this function do?"
cat error.log | claude -p "explain this error"
```

## 核心标志（8个）

| 标志 | 做什么 | 什么时候用 |
|------|--------|-----------|
| `-p, --print` | 打印模式，输出后退出 | 脚本、CI/CD、管道 |
| `-c, --continue` | 继续最近一次会话 | 断点续传 |
| `-r, --resume` | 按ID或名称恢复指定会话 | 切换任务 |
| `--model` | 指定模型（opus/sonnet/haiku） | 复杂任务换强力模型 |
| `--output-format` | 输出格式（text/json/stream-json） | 需要结构化输出 |
| `--permission-mode` | 权限模式（plan/acceptEdits/auto） | 控制安全级别 |
| `--max-turns` | 限制自动化轮次 | 控制花费/防止跑偏 |
| `--agents` | 定义自定义 subagents（JSON） | 定制工作流 |

## 权限模式

控制 Claude Code 能做什么的关键开关：

| 模式 | 行为 | 什么时候用 |
|------|------|-----------|
| `plan` | 只读（Read/Grep/Glob） | 代码审查、安全审计 |
| `acceptEdits` | 编辑文件需确认 | 日常开发（默认） |
| `auto` | 自动批准所有工具 | 信任的自动化场景 |

> [查看权限模式决策流](assets/permission-decision.html)

```bash
# 只读审查
claude --permission-mode plan "review this codebase"

# 阻止危险命令
claude --disallowedTools "Bash(rm:*)" "Bash(git push --force:*)"
```

## 会话管理

3 种方式在不同场景间切换：

| 操作 | 命令 | 场景 |
|------|------|------|
| 继续上次 | `claude -c` | 断点续传 |
| 恢复指定 | `claude -r "feature-auth"` | 多任务切换 |
| 分叉试验 | `claude --resume abc --fork-session` | 尝试替代方案，原会话不变 |

> [查看会话状态轮转](assets/session-lifecycle.html)

## 打印模式三板斧

| 场景 | 命令 | 一句话 |
|------|------|--------|
| 审查代码 | `cat file \| claude -p "review"` | 管道传入文件，AI 审查 |
| JSON 输出 | `claude -p --output-format json "query" \| jq` | 结构化输出，脚本消费 |
| 限制花费 | `claude -p --max-turns 3 "query"` | 控制轮次，防止超支 |

> [查看交互式演示](assets/print-mode-trifecta.html)

## 模型选择速查

```bash
claude --model opus "复杂的架构审查"     # 最强
claude --model sonnet "实现这个功能"      # 日常默认
claude --model haiku -p "格式化JSON"      # 快速便宜
```

## 三要三不要

| ✅ 要 | ❌ 不要 |
|------|--------|
| 日常开发用 `claude` 进入 REPL | 忘记 `-c` 硬着头皮重开新会话 |
| 脚本/CI 用 `-p` 打印模式 | 交互模式里用 `-p`（互斥） |
| 尝试新方案前 `--fork-session` | 不设 `--max-turns` 就跑长时间自动化 |

## 其他标记为"用的时候再查"

- MCP 详细配置 → [05-mcp](../05-mcp/)
- Agents 完整定义 → [04-subagents](../04-subagents/)
- CI/CD 完整示例 → 需要时参考 `zh/10-cli/README.md`
- 环境变量完整列表 → 查表即可
- 故障排查 → 遇到再看

---

## 相关资源

- [10-cli 完整教程](../../zh/10-cli/README.md) — 仓库原始教程
- [学习方法论](../learning-methodology/README.md) — 本文所用的方法论
- [官方 CLI 参考](https://code.claude.com/docs/en/cli-reference)

---

**Last Updated**: May 31, 2026
**Claude Code Version**: 2.1.150
**来源**: `zh/10-cli/README.md`
