# Checkpoints 核心知识

> 用二八法则学习方法论从官方文档和教程中提炼的 20% 核心知识。详细内容见 [08-checkpoints 完整教程](../../zh/08-checkpoints/README.md)。

## 一句话定义

Checkpoints 是 Claude Code 的自动快照机制——每次用户输入自动保存会话状态（消息+文件修改+上下文），可随时回退。

## 核心概念

| 概念 | 定义 |
|------|------|
| **Checkpoint** | 会话状态快照，含消息历史、文件修改、工具调用记录 |
| **Rewind** | 回到之前的 Checkpoint，撤销后续的代码/对话修改 |
| **Summarize** | AI 压缩对话内容为摘要，释放上下文窗口，不改文件 |

### 访问方式

| 方式 | 操作 |
|------|------|
| 快捷键 | `Esc` + `Esc`（输入框为空时） |
| 命令 | `/rewind` |
| 别名 | `/checkpoint` |

## 6 个回退选项

| 选项 | 做什么 | 什么时候用 |
|------|--------|-----------|
| **恢复代码和对话** | 代码和对话都回到该点 | 想彻底重新来过 |
| **恢复对话** | 只回退对话历史 | 代码改对了，话说错了，重说 |
| **恢复代码** | 只回退文件修改 | 话说对了，代码改坏了，重写 |
| **从此处总结** | 该点之后的对话压缩为摘要 | 上下文快满了，释放空间 |
| **到此处总结** | 该点之前的对话压缩为摘要 | 前面的讨论太长，压缩掉 |
| **算了** | 取消，不做任何操作 | 手滑了，不想回退 |

> [查看交互式选项对比](assets/rewind-options.html)

## 4 个核心使用场景

| 场景 | 工作流 |
|------|--------|
| **探索替代方案** | 动手前（自动存）→ 试方案 A → 回退 → 试方案 B → 对比 → 选最优 |
| **错误恢复** | 发现改坏了 → `Esc+Esc` → 回退到正常状态 |
| **安全重构** | 重构前（自动存）→ 改 → 跑测试 → 失败就回退 |
| **释放上下文** | 对话太长 → 在合适位置"从此处总结" → 继续工作 |

> [查看工作流动画演示](assets/workflow-patterns.html)

## 关键限制 + 三要三不要

### 关键限制

1. **Bash 命令不跟踪**：`rm`/`mv`/`cp` 等文件操作无法通过 Rewind 撤销
2. **外部修改不跟踪**：在编辑器/终端中手动改的文件不在 Checkpoint 覆盖范围
3. **不是 Git 替代品**：Checkpoints = 本地快速回退，Git = 永久版本历史

> [查看恢复 vs 总结差异对比](assets/restore-vs-summarize.html)

### 三要三不要

| ✅ 要 | ❌ 不要 |
|------|--------|
| 用 Checkpoints 做快速实验 | 把它当 Git 替代品 |
| 上下文紧张时用"总结"释放空间 | 依赖它跟踪 bash 命令改动 |
| 确认满意的方案后 commit 到 Git | 依赖它跟踪外部编辑器的改动 |

---

## 延伸阅读

- [完整教程：08-checkpoints/README.md](../../zh/08-checkpoints/README.md)
- [中文示例：checkpoint-examples.md](../../zh/08-checkpoints/checkpoint-examples.md)
- [官方文档：Checkpointing](https://code.claude.com/docs/zh-CN/checkpointing)

---

**Last Updated**: May 31, 2026
**Claude Code Version**: 2.1.150
**Sources**:
- https://code.claude.com/docs/en/checkpointing
- 08-checkpoints/README.md
- zh/08-checkpoints/checkpoint-examples.md
**Compatible Models**: Claude Sonnet 4.6, Claude Opus 4.7, Claude Haiku 4.5
