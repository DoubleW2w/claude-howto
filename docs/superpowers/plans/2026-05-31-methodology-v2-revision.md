# 方法论可视化标准 v2 修订 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将学习方法的可视化决策标准从 v1（3条条件）升级到 v2（6条条件+不确定问用户铁律），同步更新方法论框架的两份核心文件。

**Architecture:** 两处增量编辑——README 替换第四步半决策表+新陷阱+铁律，prompt-templates 的模板4同步v2标准。不涉及任何具体知识点的内容变更。

**Tech Stack:** Markdown 编辑

---

### Task 1: 更新 `learning-methodology/README.md` — 第四步半决策表

**Files:**
- Modify: `my-learning/learning-methodology/README.md`

- [ ] **Step 1: 替换第四步半的可视化决策表**

找到"第四步半：可视化检查"下的旧决策表，替换为新表。

旧表（4行，含CLI示例列）：
```markdown
| 条件 | 生成？ | CLI 示例 |
|------|--------|---------|
| 概念是**空间/流程关系**（分支、回退、对比） | ✅ | — |
| **表格不足以传达**决策逻辑 | ✅ | — |
| 两个概念**容易混淆**，需并列对比 | ✅ | 交互模式 vs 打印模式 → 可以用 HTML |
| 纯**文本/命令/配置**，表格够用 | ❌ | CLI 命令列表、标志表、权限模式 → 表格足够 |
```

新表（6行，去掉CLI示例列，改为说明列）：
```markdown
| 条件 | 决策 | 说明 |
|------|------|------|
| 纯命令列表、纯配置值、纯文本 | ❌ 不生成 HTML | CLI 标志表、环境变量表、API 参数表 |
| 概念易混淆，需并列对比帮助理解 | ✅ 生成 HTML | 恢复 vs 总结、交互模式 vs 打印模式 |
| 场景描述 / 案例演示，**文字量大且不直观** | ✅ 生成 HTML | 文字阐述冗长时用动画替代 |
| 工作流 / 分支决策 / 状态轮转 | ✅ 生成 HTML | 权限模式选择路径、会话分叉流程 |
| 变化过程 / 数据流动 / 前后差异 | ✅ 生成 HTML | 管道串联、JSON 输出转换、重构前后 |
| **不确定属于哪类** | ⚠️ **必须询问用户** | 禁止自行猜测。问"这里需要生成可视化吗？" |
```

- [ ] **Step 2: 在决策表后追加"不确定问用户"铁律**

在决策表后、Prompt模板链接前插入：
```markdown
> **铁律**：判断不准时，问用户。不猜。不假设。"这里需要可视化吗？你觉得文字描述够清晰吗？"
```

- [ ] **Step 3: 新增第5条常见陷阱**

在常见陷阱表末尾追加一行：
```markdown
| 跳过可视化检查 | 完成文档后直接结束，没有对照决策表 | 第四步半是强制步骤，完成文档后立即检查 |
```

- [ ] **Step 4: 验证**

```bash
grep -c "必须询问用户" my-learning/learning-methodology/README.md
grep -c "跳过可视化检查" my-learning/learning-methodology/README.md
```

Expected: 均 ≥1

---

### Task 2: 更新 `learning-methodology/prompt-templates.md` — 模板4同步v2

**Files:**
- Modify: `my-learning/learning-methodology/prompt-templates.md`

- [ ] **Step 1: 替换模板4的可视化检查标准**

找到模板4 Prompt中的第四步条件列表（当前5行），替换为v2的6条标准。

旧版：
```text
第四步（可视化检查）：根据以下标准，判断是否需要生成交互式 HTML 可视化：
- 概念之间是空间/流程关系（分支、回退、对比）→ ✅ 生成
- 表格不足以传达决策逻辑 → ✅ 生成
- 两个概念容易混淆，需并列对比 → ✅ 生成
- 代码块里描述具体场景时 -> ✅ 生成
- 纯文本/命令/配置，表格够用 → ❌ 不生成
```

新版：
```text
第四步（可视化检查）：根据以下标准，判断是否需要生成交互式 HTML 可视化：
- 纯命令列表、纯配置值、纯文本 → ❌ 不生成
- 概念易混淆，需并列对比帮助理解 → ✅ 生成
- 场景描述/案例演示，文字量大且不直观 → ✅ 生成
- 工作流/分支决策/状态轮转 → ✅ 生成
- 变化过程/数据流动/前后差异 → ✅ 生成
- 不确定属于哪类 → ⚠️ 必须询问用户，禁止自行判断
```

- [ ] **Step 2: 同步更新格式要求**

确保模板4的格式要求包含：
```text
格式要求：文档开头必须包含可视化决策记录，格式为：
> **可视化决策**：[生成/不生成] HTML。[生成文件数] 个。理由：[一句话]。
> 如有不确定触发，已在实施过程中向用户确认。
```

- [ ] **Step 3: 验证**

```bash
grep -c "必须询问用户" my-learning/learning-methodology/prompt-templates.md
grep -c "文字量大且不直观" my-learning/learning-methodology/prompt-templates.md
```

Expected: 均 ≥1

---

### Task 3: 质量验证

**Files:**
- Check: `my-learning/learning-methodology/README.md`
- Check: `my-learning/learning-methodology/prompt-templates.md`

- [ ] **Step 1: 验证两份文件的v2标准一致性**

```bash
echo "=== README ==="
grep -c "文字量大且不直观\|必须询问用户\|纯命令列表" my-learning/learning-methodology/README.md
echo "=== Prompt Templates ==="
grep -c "文字量大且不直观\|必须询问用户\|纯命令列表" my-learning/learning-methodology/prompt-templates.md
```

Expected: 均 ≥2（每条标准至少匹配一次）。

- [ ] **Step 2: Markdown无内嵌HTML**

```bash
grep -rln '<\(html\|style\|script\|div\|iframe\)' my-learning/learning-methodology/*.md
```

Expected: 无匹配。

- [ ] **Step 3: 链接有效性**

```bash
ls my-learning/learning-methodology/prompt-templates.md
ls my-learning/learning-methodology/assets/pareto-vs-occam.html
ls my-learning/learning-methodology/assets/methodology-flow.html
```

Expected: 全部存在。
