<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../../resources/logos/claude-howto-logo.svg">
</picture>

# Checkpoints 与 Rewind

Checkpoints 允许你在 Claude Code 会话中保存对话状态并回退到之前的任意时间点。这在探索不同方案、从错误中恢复或比较替代实现时非常有用。

## 概览

Checkpoints 允许你保存对话状态并回退到之前的时间点，从而安全地进行试验和探索多种方案。它们是对话状态的快照，包含：
- 所有已交换的消息
- 已做出的文件修改
- 工具使用历史
- 会话上下文

在探索不同方案、从错误中恢复或比较替代方案时，Checkpoints 非常重要。

## 核心概念

| 概念 | 说明 |
|---------|-------------|
| **Checkpoint** | 对话状态的快照，包含消息、文件和上下文 |
| **Rewind** | 回到之前的 checkpoint，丢弃之后的所有更改 |
| **Branch Point** | 以此为起点探索多个方案的 checkpoint |

## 访问 Checkpoints

你可以通过两种主要方式访问和管理 checkpoints：

### 使用键盘快捷键
按两次 `Esc`（`Esc` + `Esc`）打开 checkpoint 界面并浏览已保存的 checkpoints。

### 使用 Slash Command
使用 `/rewind` 命令（别名：`/checkpoint`）快速访问：

```bash
# 打开 rewind 界面
/rewind

# 或者使用别名
/checkpoint
```

## Rewind 选项

回退时，系统会提供五个选项的菜单：

1. **恢复代码和对话** — 将文件和消息都恢复到该 checkpoint 的状态
2. **恢复对话** — 只回退消息，保留当前代码不变
3. **恢复代码** — 只回退文件修改，保留完整对话历史
4. **从这里开始总结** — 将从此处往后的对话压缩为 AI 生成的摘要，释放上下文窗口空间。所选位置之前的所有消息保持不变。磁盘上的文件不受影响。原始消息仍保留在会话记录中。你可以额外提供指令，让摘要聚焦于特定主题。
5. **算了** — 取消并返回当前状态

> **注意**：恢复对话或进行总结后，所选消息的原始提示会恢复到输入框中，以便你重新发送或编辑。

## 自动 Checkpoints

Claude Code 会自动为你创建 checkpoints：

- **每次用户提示** — 每次用户输入都会创建一个新的 checkpoint
- **持久保存** — Checkpoints 跨会话保留
- **自动清理** — Checkpoints 会在 30 天后自动清理

这意味着你随时都可以回退到对话中的任意节点——无论是几分钟前还是几天前。

## 使用场景

| 场景 | 工作流 |
|----------|----------|
| **探索不同方案** | 保存 → 尝试方案 A → 保存 → Rewind → 尝试方案 B → 比较 |
| **安全重构** | 保存 → 重构 → 测试 → 如果失败：Rewind |
| **A/B 测试** | 保存 → 设计 A → 保存 → Rewind → 设计 B → 比较 |
| **错误恢复** | 发现问题 → Rewind 到最后一个正常状态 |

## 使用 Checkpoints

### 查看与回退

按两次 `Esc` 或使用 `/rewind` 打开 checkpoint 浏览器。你会看到一个包含时间戳的可用 checkpoint 列表。选择任意 checkpoint 即可回退到该状态。

### Checkpoint 详情

每个 checkpoint 会显示：
- 创建时间戳
- 被修改的文件
- 对话中的消息数量
- 使用过的工具

## 实战示例

### 示例 1：探索不同方案

```
User: 我们给 API 加一个缓存层吧

Claude: 我来为你的 API 端点添加 Redis 缓存……
[在 checkpoint A 处做出修改]

User: 其实不如试试内存缓存

Claude: 我 rewind 回去，换个方案试……
[用户按下 Esc+Esc 并回退到 checkpoint A]
[在 checkpoint B 处实现内存缓存]

User: 现在我可以比较两种方案了
```

### 示例 2：从错误中恢复

```
User: 把认证模块重构成基于 JWT 的实现

Claude: 我来重构认证模块……
[做出大量修改]

User: 等等，这把 OAuth 集成弄坏了。退回去。

Claude: 我来帮你回退到重构之前……
[用户按下 Esc+Esc，选择重构之前的 checkpoint]

User: 这次我们试一个更保守的方案
```

### 示例 3：安全试验

```
User: 我们试试把它改写成函数式风格
[在试验前创建 checkpoint]

Claude: [做出试验性修改]

User: 测试失败了。回退吧。
[用户按下 Esc+Esc 并回退到 checkpoint]

Claude: 更改已回退。我们换个方案试试。
```

### 示例 4：分支式探索

```
User: 我想比较两种数据库设计
[记下当前的 checkpoint — 称为 "Start"]

Claude: 我来实现第一种设计……
[实现 Schema A]

User: 现在让我回去试第二种方案
[用户按下 Esc+Esc 并回退到 "Start"]

Claude: 现在我来实现 Schema B……
[实现 Schema B]

User: 太好了！现在两个 schema 可供选择了
```

## Checkpoint 保留策略

Claude Code 会自动管理你的 checkpoints：

- 每次用户输入都会自动创建 checkpoint
- 旧 checkpoint 最多保留 30 天
- 系统会自动清理 checkpoint，防止存储空间无限增长

## 工作流模式

### 探索时的分支策略

在探索多种方案时：

```
1. 从初始实现开始 → Checkpoint A
2. 尝试方案 1 → Checkpoint B
3. 回退到 Checkpoint A
4. 尝试方案 2 → Checkpoint C
5. 比较 B 和 C 的结果
6. 选择最佳方案并继续
```

### 安全重构模式

在进行重大修改时：

```
1. 当前状态 → Checkpoint（自动）
2. 开始重构
3. 运行测试
4. 如果测试通过 → 继续工作
5. 如果测试失败 → Rewind 并尝试其他方案
```

## 最佳实践

由于 checkpoints 是自动创建的，你可以专注工作而无需担心手动保存状态。但以下实践仍需注意：

### 高效使用 Checkpoints

✅ **推荐：**
- 回退前先查看可用的 checkpoints
- 想探索不同方向时使用 rewind
- 保留 checkpoints 以比较不同方案
- 理解每个 rewind 选项的作用（恢复代码和对话、恢复对话、恢复代码、或总结）

❌ **避免：**
- 仅依赖 checkpoints 来保存代码
- 指望 checkpoints 跟踪外部文件系统的变更
- 将 checkpoints 当作 git commit 的替代品

## 配置

Checkpoints 是 Claude Code 的内置默认行为，无需任何配置即可启用。每次用户提示都会自动创建 checkpoint。

唯一与 checkpoint 相关的设置是 `cleanupPeriodDays`，用于控制会话和 checkpoints 的保留时长：

```json
{
  "cleanupPeriodDays": 30
}
```

- `cleanupPeriodDays`：会话历史和 checkpoints 的保留天数（默认：`30`）

> **v2.1.117 更新**：`cleanupPeriodDays` 现在统一管理四类磁盘缓存的保留，而不仅仅是 checkpoints：
>
> - 会话 checkpoints
> - `~/.claude/tasks/` — 持久化任务列表
> - `~/.claude/shell-snapshots/` — 捕获的 shell 环境快照
> - `~/.claude/backups/` — 设置 / CLAUDE.md 的滚动备份
>
> 现在只需一项设置即可在相同天数后统一清理这四个目录。

## 局限性

Checkpoints 存在以下局限性：

- **Bash 命令变更不会被跟踪** — 文件系统上的 `rm`、`mv`、`cp` 等操作不会被 capture 到 checkpoints 中
- **外部变更不会被跟踪** — 在 Claude Code 之外（编辑器、终端等）做出的修改不会被 capture
- **不能替代版本控制** — 请使用 git 来进行永久、可审计的代码库变更

## 故障排查

### 找不到 Checkpoints

**问题**：预期的 checkpoint 未找到

**解决方案**：
- 检查 checkpoints 是否已被清理
- 检查磁盘空间
- 确保 `cleanupPeriodDays` 设置得足够大（默认：30 天）

### Rewind 失败

**问题**：无法回退到 checkpoint

**解决方案**：
- 确保没有未提交的变更产生冲突
- 检查 checkpoint 是否已损坏
- 尝试回退到其他 checkpoint

## 与 Git 集成

Checkpoints 是 git 的补充（而非替代）：

| 功能 | Git | Checkpoints |
|---------|-----|-------------|
| 范围 | 文件系统 | 对话 + 文件 |
| 持久性 | 永久 | 基于会话 |
| 粒度 | 按 commit | 任意时间点 |
| 速度 | 较慢 | 即时 |
| 共享 | 支持 | 有限 |

两者结合使用：
1. 使用 checkpoints 快速迭代试验
2. 使用 git commit 保存最终确认的修改
3. 在执行 git 操作前创建 checkpoint
4. 将成功的 checkpoint 状态提交到 git

## 快速开始指南

### 基本工作流

1. **正常使用** — Claude Code 自动创建 checkpoints
2. **想回退？** — 按两次 `Esc` 或使用 `/rewind`
3. **选择 checkpoint** — 从列表中选取要回退到的 checkpoint
4. **选择恢复内容** — 从恢复代码和对话、恢复对话、恢复代码、从这里开始总结或取消中选择
5. **继续工作** — 你已经回到那个时间点了

### 键盘快捷键

- **`Esc` + `Esc`** — 打开 checkpoint 浏览器
- **`/rewind`** — 另一种访问 checkpoints 的方式
- **`/checkpoint`** — `/rewind` 的别名

## 何时该 Rewind：上下文监控

Checkpoints 让你能回退——但如何判断*什么时候*该回退呢？随着对话增长，Claude 的上下文窗口会被填满，模型质量也会悄然下降。你可能正在和一个半盲的模型一起写代码，却浑然不知。

**[cc-context-stats](https://github.com/luongnv89/cc-context-stats)** 通过在 Claude Code 状态栏中添加实时**上下文区间**来解决这个问题。它会追踪你在上下文窗口中的位置——从 **Plan**（绿色，安全进行规划和编码）到 **Code**（黄色，避免启动新计划）再到 **Dump**（橙色，收尾并 rewind）。当区间发生变化时，你就知道是时候创建 checkpoint 并重新开始了，而不是在输出质量下降时硬撑。

## 相关概念

- **[Advanced Features](../09-advanced-features/)** — Planning mode 及其他高级功能
- **[Memory Management](../02-memory/)** — 对话历史与上下文管理
- **[Slash Commands](../01-slash-commands/)** — 用户调用的快捷命令
- **[Hooks](../06-hooks/)** — 事件驱动自动化
- **[Plugins](../07-plugins/)** — 打包的扩展功能

## 更多资源

- [官方 Checkpointing 文档](https://code.claude.com/docs/en/checkpointing)
- [Advanced Features Guide](../09-advanced-features/) — Extended thinking 及其他功能

## 总结

Checkpoints 是 Claude Code 的内置自动功能，让你可以安全地探索不同方案而无需担心丢失工作。每次用户输入都会自动创建新的 checkpoint，因此你可以回退到会话中的任意时间点。

核心优势：
- 无畏地试验多种方案
- 快速从错误中恢复
- 并排比较不同解决方案
- 与版本控制系统安全集成

请记住：checkpoints 不能替代 git。使用 checkpoints 进行快速试验，使用 git 进行永久代码变更。

---

**最后更新**：2026 年 5 月 25 日
**Claude Code 版本**：2.1.150
**来源**：
- https://code.claude.com/docs/en/checkpointing
- https://code.claude.com/docs/en/settings
- https://github.com/anthropics/claude-code/releases/tag/v2.1.117
**兼容模型**：Claude Sonnet 4.6、Claude Opus 4.7、Claude Haiku 4.5
