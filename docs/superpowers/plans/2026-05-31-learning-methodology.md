# 学习方法论 + Checkpoints 核心知识 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `my-learning/` 下建立两套独立文档：可复用的二八法则+奥卡姆剃刀学习方法论，以及用该方法论提炼的 Checkpoints 核心知识。

**Architecture:** 两份独立 Markdown 文档（methodology + checkpoints），各自配 prompt 模板和按需生成的 HTML 视觉文件。HTML 使用 frontend-design + huashu-design 技能制作精美动画交互。Markdown 通过相对链接引用 HTML，不内嵌 HTML 代码。

**Tech Stack:** Markdown, HTML/CSS/JS（单文件自包含）, frontend-design skill, huashu-design skill, visual-companion server for preview

---

## 文件结构

```
my-learning/
├── learning-methodology/
│   ├── README.md                      # 新建：方法论正文
│   ├── prompt-templates.md            # 新建：4个Prompt模板
│   └── assets/                        # 新建：HTML视觉文件
│       ├── methodology-flow.html      # 4步方法论动画流程图
│       └── pareto-vs-occam.html       # 二八法则vs奥卡姆剃刀对比
└── checkpoints/
    ├── README.md                      # 新建：Checkpoints核心知识
    └── assets/                        # 新建：HTML视觉文件
        ├── rewind-options.html        # 6个回退选项交互卡片
        ├── workflow-patterns.html     # 4个工作流动画流程图
        └── restore-vs-summarize.html  # 恢复vs总结差异对比
```

---

### Task 1: 创建目录结构

**Files:**
- Create: `my-learning/learning-methodology/assets/` (directory)
- Create: `my-learning/checkpoints/assets/` (directory)

- [ ] **Step 1: 创建所有目录**

```bash
mkdir -p my-learning/learning-methodology/assets
mkdir -p my-learning/checkpoints/assets
```

- [ ] **Step 2: 验证目录结构**

```bash
ls -la my-learning/learning-methodology/
ls -la my-learning/checkpoints/
```

Expected: 两个目录均存在，含 `assets/` 子目录。

- [ ] **Step 3: Commit**

```bash
git add my-learning/
git commit -m "chore(learning): create my-learning directory structure"
```

---

### Task 2: 编写 `learning-methodology/README.md`

**Files:**
- Create: `my-learning/learning-methodology/README.md`

**Source references:**
- Spec sections: "1. learning-methodology/README.md" (7 parts, ~1500字)
- 官方文档: `https://code.claude.com/docs/zh-CN/checkpointing`
- 仓库: `08-checkpoints/README.md`

- [ ] **Step 1: 编写 Part 1 — 核心理念（~200字）**

写入内容结构：
```
# 快速掌握任何领域的核心知识

## 核心理念

两条原则，一个目标：用最少时间掌握能解决大部分问题的知识。

**二八法则（帕累托法则）**
20% 的核心知识能覆盖 80% 的使用场景。找那 20%，跳过其余 80%。

**奥卡姆剃刀**
如无必要，勿增实体。能用一句话讲清的，不写一段话。能用一个例子的，不给三个。

**组合使用**
二八法则定位"学什么"，奥卡姆剃刀决定"怎么学"。一个聚焦重点，一个砍掉废话。
```

- [ ] **Step 2: 编写 Part 2 — 四步操作法（~300字）**

写入内容：
```
## 四步操作法

### 第一步：定位信息源
找到权威、完整的信息源。官方文档 > 优质教程 > 博客文章。2-3个即可，多了分散注意力。

### 第二步：抓取骨骼
只看骨架，不看血肉：
- 浏览目录和标题结构
- 列出核心概念（≤10 个）
- 提取关键 API / 命令表
- 记录配置项清单
这一步禁止深入阅读正文。

### 第三步：提取核心
应用二八法则：从骨骼中筛出 4-6 张核心概念卡。
判断标准：
- 这个知识点，我接下来 80% 的日常操作会用到吗？
- 不用它，我是否无法入门？
两个问题都回答"是"→ 放入核心。否则 → 标记为"用的时候再查"。

### 第四步：去噪成文
应用奥卡姆剃刀：
- 删除重复的解释性段落
- 删除"这个功能很重要"等评价性语言
- 每个概念只保留一个最简示例
- 保留所有必要的技术细节和命令
终止条件：如果信息源本身已经精炼，不要为了压缩而压缩。边际价值递减。

> 详细 Prompt 模板见 [prompt-templates.md](prompt-templates.md)
```

- [ ] **Step 3: 编写 Part 3 — 完整演示：Checkpoints（~500字）**

写入内容：
```
## 完整演示：用四步法学习 Checkpoints

以下展示从"零基础"到"掌握核心知识"的完整过程。

### 第一步：定位信息源
- `08-checkpoints/README.md` — 仓库教程，335行，覆盖全面
- `code.claude.com/docs/zh-CN/checkpointing` — 官方文档，权威但精简

### 第二步：抓取骨骼

从两份文档提取结构骨架：

| 类别 | 内容 |
|------|------|
| 核心概念 | Checkpoint（快照）、Rewind（回退）、Summarize（总结） |
| 入口方式 | `Esc+Esc`、`/rewind`、`/checkpoint` |
| 回退选项 | 恢复代码和对话、恢复对话、恢复代码、从此处总结、到此处总结、取消 |
| 使用场景 | 探索替代方案、错误恢复、功能迭代、释放上下文 |
| 限制 | Bash命令不跟踪、外部修改不跟踪、非Git替代品 |
| 配置 | `cleanupPeriodDays`（默认30天） |

### 第三步：提取核心

应用二八法则筛选：

✅ 保留（用二八法则判断为"必知"）：
- **3个核心概念**：知道你每次都在操作什么
- **3种入口方式**：知道怎么打开
- **6个回退选项**：知道每个按钮做什么 —— 这是 80% 使用场景的关键
- **4个核心场景**：知道什么时候用

❌ 标记为"用的时候再查"：
- 自动创建机制（不需要手动操作）
- 清理周期配置（默认值够用）
- 故障排查（遇到再说）
- 配置细节（`cleanupPeriodDays` 改个数字而已）

保留率：约 25%（335行 → ~80行核心）

### 第四步：去噪成文

砍掉的内容：
- "Checkpoints 是 invaluable 的"等评价语
- 多个功能相似的示例
- 重复出现的自动机制描述

保留的内容：所有技术细节（快捷键、命令、选项定义）

最终产出：[checkpoints/README.md](../checkpoints/README.md)
```

- [ ] **Step 4: 编写 Part 4 — 核心概念卡（~300字）**

写入内容：
```
## 核心概念卡

### 二八法则操作卡

| 维度 | 内容 |
|------|------|
| **一句话** | 20% 的知识解决 80% 的问题 |
| **适用场景** | 新工具、新框架、新语言、新概念的学习 |
| **操作要诀** | 先看目录→标高频项→只学高频项→其余查阅 |
| **判断标准** | "这个知识点，我下一周会用到几次？" 少于1次→跳过 |
| **反例** | 学 Git 从内部实现开始而不是 add/commit/push |

### 奥卡姆剃刀操作卡

| 维度 | 内容 |
|------|------|
| **一句话** | 如无必要，勿增实体 |
| **适用场景** | 组织笔记、编写文档、设计解释 |
| **操作要诀** | 写完后自问"删掉这段，读者还能理解吗？" |
| **何时不用** | 安全警告、精确的法律/医学信息、API 参考文档 |
| **反例** | 为了"简洁"删掉 `rm -rf` 的危险提示 |

> [查看交互式对比演示](assets/pareto-vs-occam.html)
```

- [ ] **Step 5: 编写 Part 5 — 常见陷阱（~200字）**

写入内容：
```
## 常见陷阱

| 陷阱 | 表现 | 解决方案 |
|------|------|---------|
| **过度精简** | 砍掉了理解核心概念所必需的上下文 | 核心概念至少保留一个可运行的完整示例 |
| **伪核心** | 把"目录"当"核心知识"，只会列标题 | 核心 ≠ 索引。每条核心必须包含具体用法 |
| **一成不变** | 对所有领域用同一套筛选标准 | 工具的 20% 是常用命令；框架的 20% 是核心概念+数据流 |
| **边际价值递减** | 对已经精炼的内容继续压缩 | 原始资料已精简时，不再强行砍内容。只做结构重排 |
```

- [ ] **Step 6: 编写 Part 6 — 适用边界（~150字）**

写入内容：
```
## 适用边界

✅ **最适合**：
- 工具类知识（CLI 工具、IDE、DevOps）
- 框架类知识（React、Spring、Django）
- 概念类知识（设计模式、系统架构）

⚠️ **谨慎使用**：
- 医学、法律等需要精确完整性的领域
- 安全相关的操作指南
- 考试备考（考试可能考那 80%）

🎯 **经验法则**：如果"用错会出事"的知识，不适用此方法论。
```

- [ ] **Step 7: 编写 Part 7 — Prompt 模板入口 + 页脚**

写入内容：
```
## 工具：Prompt 模板

4 个可直接复制的 Prompt 模板覆盖四步法的每一步。详见：

→ [prompt-templates.md](prompt-templates.md)

---

## 相关资源

- [Checkpoints 核心知识](../checkpoints/README.md) — 本方法论的首个实践案例
- [08-checkpoints 完整教程](../../08-checkpoints/README.md) — 仓库原始教程
- [Claude Code 官方文档](https://code.claude.com/docs/zh-CN/checkpointing)

---

**Last Updated**: May 31, 2026
```

- [ ] **Step 8: 验证文件完整性**

```bash
wc -w my-learning/learning-methodology/README.md
```

Expected: ~1500 中文字含量（约 2000-2500 行内词数，因中文单字为一词）。

- [ ] **Step 9: Commit**

```bash
git add my-learning/learning-methodology/README.md
git commit -m "docs(learning): add learning methodology README"
```

---

### Task 3: 编写 `learning-methodology/prompt-templates.md`

**Files:**
- Create: `my-learning/learning-methodology/prompt-templates.md`

- [ ] **Step 1: 编写文件头部和模板1 — 骨骼提取**

写入内容：
```
# Prompt 模板

4 个可直接复制使用的 Prompt 模板，对应四步操作法。所有示例输出均用 Checkpoints 演示。

---

## 模板 1：骨骼提取

**用途**：第二步"抓取骨骼"——只提取结构，不看正文。

**适用场景**：手头有文档/网页/教程，需要快速建立知识地图。

### Prompt

```
分析以下文档，只提取结构信息，不要正文内容：

1. 完整的目录树（含所有标题层级）
2. 核心概念列表（≤10 个，每个一行）
3. 关键命令/API/快捷键表（如有）
4. 配置项/设置项清单（如有）

输出格式：Markdown 表格和列表。禁止输出解释性文字。
```

### Checkpoints 示例输出

**目录树：**
- Checkpoints and Rewind
  - Overview
  - Key Concepts
  - Accessing Checkpoints
  - Rewind Options
  - Automatic Checkpoints
  - Use Cases
  - Using Checkpoints
  - Practical Examples
  - Workflow Patterns
  - Best Practices
  - Configuration
  - Limitations
  - Troubleshooting
  - Integration with Git

**核心概念（3个）：**
| 概念 | 一句话 |
|------|--------|
| Checkpoint | 会话状态快照（消息+文件+上下文） |
| Rewind | 回退到指定快照 |
| Summarize | 压缩对话释放上下文窗口 |

**关键入口（3种）：**
| 方式 | 操作 |
|------|------|
| 快捷键 | `Esc` + `Esc` |
| 命令 | `/rewind` |
| 别名 | `/checkpoint` |

**配置项（1个）：**
| 配置 | 默认值 | 说明 |
|------|--------|------|
| `cleanupPeriodDays` | 30 | 清理周期（天） |

---

## 模板 2：核心提炼

**用途**：第三步"提取核心"——用二八法则从骨骼中筛出必知内容。

**适用场景**：已完成骨骼提取，需要进一步聚焦。

### Prompt

```
以下是我对 [领域名称] 的骨骼分析。请应用二八法则做核心提炼：

骨骼内容：
[粘贴模板1的输出]

要求：
1. 从核心概念中只筛选 4-6 个"必须掌握"的，给出判断理由
2. 标记哪些内容是"用的时候再查"级别的
3. 为每个核心概念写一张概念卡（名称、一句话定义、最简用法示例）
4. 最终保留率控制在 20-30%

输出格式：Markdown，每个概念卡用 ### 标题。
```

### Checkpoints 示例输出

**核心概念卡（4张）：**

### 1. Checkpoint（快照）

**定义**：每次用户输入时自动创建的会话状态快照，包含消息历史、文件修改、工具调用记录。

**最简用法**：无需手动操作，Claude Code 自动创建。

---

### 2. Rewind（回退）

**定义**：回到之前的 Checkpoint，有 6 种操作可选。

**最简用法**：按 `Esc+Esc` → 选 Checkpoint → 选操作 → 确认。

---

### 3. 回退选项（6种）

**定义**：回退时的 6 个菜单选项。

**最简用法**：
| 选项 | 用的时候 |
|------|---------|
| 恢复代码和对话 | 想彻底回到某一步 |
| 恢复对话 | 代码留着，对话回退 |
| 恢复代码 | 对话留着，代码回退 |
| 从此处总结 | 上下文满了，压缩后面 |
| 到此处总结 | 压缩前面的废话 |
| 算了 | 手滑了 |

---

### 4. 使用场景（4种）

**定义**：最适合用 Checkpoints 的典型工作流。

**最简用法**：
- 探索替代方案 → 存快照 → 试 A → 回退 → 试 B → 对比
- 错误恢复 → 发现改坏了 → 回退到好的状态
- 上下文管理 → 上下文满了 → 总结释放空间

**标记为"用的时候再查"：**
- 自动创建机制（透明行为，不需要理解）
- 清理周期配置（`cleanupPeriodDays: 30` 够用）
- 故障排查（遇到再查）

保留率：~25%

---

## 模板 3：去噪精简

**用途**：第四步"去噪成文"——砍掉废话，保留实质。

**适用场景**：已提取核心内容，需要整理成最终笔记。

### Prompt

```
将以下内容精简为最简可用版本。

原始内容：
[粘贴模板2的输出或自己的笔记]

精简规则：
1. 删除所有评价性语言（"很重要""非常有用""不可或缺"等）
2. 删除重复的解释段落
3. 每个概念只保留一个最简示例
4. 保留所有技术细节（命令、快捷键、配置值、限制说明）
5. 如果原始内容已经足够精炼，不要为了压缩而压缩

输出格式：干净的 Markdown。
```

### Checkpoints 示例输出

精简前（评价性语言标注）：
> Checkpoints ~~are invaluable for~~ exploring different approaches...
> ~~Since checkpoints are created automatically, you can focus on your work without worrying about manually saving state.~~
> ~~This means you can always rewind to any previous point...~~

精简后：
```
Checkpoints 自动为每次用户输入创建快照。按 Esc+Esc 或 /rewind 打开回退菜单。

6 个选项：
| 恢复代码和对话 | 全回退 | 想从头重试 |
| 恢复对话       | 只退对话 | 代码对，话说错了 |
| 恢复代码       | 只退代码 | 话说对，代码写坏了 |
| 从此处总结     | 压缩后续 | 上下文满了 |
| 到此处总结     | 压缩前置 | 早期废话太多 |
| 算了           | 取消 | 手滑了 |

❌ 不跟踪 bash 命令、外部修改；不是 git 替代品。
```

---

## 模板 4：快速入门

**用途**：组合模板 1+2+3，从零掌握陌生领域。

**适用场景**：接触新工具/新框架/新概念，30 分钟内建立核心认知。

### Prompt

```
我要学习 [领域名称]。请按以下步骤帮我快速掌握核心知识：

第一步：列出该领域的骨骼结构（目录/核心概念/关键命令表/配置项表）。禁止输出正文。

第二步：用二八法则从骨骼中筛选 ≤6 个核心概念。对每个核心概念，给出：
- 名称
- 一句话定义
- 最简用法示例（一个）

第三步：列出 3 个最容易踩的坑。

输出格式：干净的 Markdown。禁止评价性语言。禁止重复。如果原始内容已经精炼，不再压缩。

参考信息源：
[粘贴或列出文档链接]
```

### Checkpoints 示例输出

（略——此模板的输出即 [checkpoints/README.md](../checkpoints/README.md) 的内容结构。）
```

- [ ] **Step 2: 验证文件完整性**

```bash
grep -c "^## 模板" my-learning/learning-methodology/prompt-templates.md
```

Expected: `4`（4个模板）。

- [ ] **Step 3: Commit**

```bash
git add my-learning/learning-methodology/prompt-templates.md
git commit -m "docs(learning): add prompt templates for methodology"
```

---

### Task 4: 编写 `checkpoints/README.md`

**Files:**
- Create: `my-learning/checkpoints/README.md`

**Source references:**
- `08-checkpoints/README.md` — 完整教程
- `zh/08-checkpoints/checkpoint-examples.md` — 中文示例
- `https://code.claude.com/docs/zh-CN/checkpointing` — 官方中文文档

- [ ] **Step 1: 编写文件**

写入内容结构（~600字）：
```
# Checkpoints 核心知识

> 用[二八法则学习方法论](../learning-methodology/README.md)从官方文档和教程中提炼的 20% 核心知识。详细内容见 [08-checkpoints 完整教程](../../08-checkpoints/README.md)。

## 一句话定义

Checkpoints 是 Claude Code 的自动快照机制——每次用户输入自动保存会话状态（消息+文件修改+上下文），可随时回退。

## 核心概念

| 概念 | 定义 |
|------|------|
| **Checkpoint** | 会话状态快照，含消息历史、文件修改、工具调用记录 |
| **Rewind** | 回到之前的 Checkpoint，撤销后续的代码/对话修改 |
| **Summarize** | AI 压缩对话内容为摘要，释放上下文窗口，不改文件 |

## 入口

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
| **探索替代方案** | 动手前 → 试方案 A → 回退 → 试方案 B → 对比 → 选最优 |
| **错误恢复** | 发现改坏了 → `Esc+Esc` → 回退到正常状态 |
| **安全重构** | 重构前（自动存）→ 改 → 跑测试 → 失败就回退 |
| **释放上下文** | 对话太长 → 在合适位置"从此处总结" → 继续工作 |

> [查看工作流动画演示](assets/workflow-patterns.html)

## 关键限制（3条）

1. **Bash 命令不跟踪**：`rm`/`mv`/`cp` 等文件操作无法通过 Rewind 撤销
2. **外部修改不跟踪**：在编辑器/终端中手动改的文件不在 Checkpoint 覆盖范围
3. **不是 Git 替代品**：Checkpoints = 本地快速回退，Git = 永久版本历史。两者配合使用

> [查看恢复 vs 总结差异对比](assets/restore-vs-summarize.html)

## 三要三不要

| ✅ 要 | ❌ 不要 |
|------|--------|
| 用 Checkpoints 做快速实验 | 把它当 Git 替代品 |
| 上下文紧张时用"总结"释放空间 | 依赖它跟踪 bash 命令改动 |
| 确认满意的方案后 commit 到 Git | 依赖它跟踪外部编辑器的改动 |

---

## 相关资源

- [08-checkpoints 完整教程](../../08-checkpoints/README.md)
- [Claude Code 官方文档](https://code.claude.com/docs/zh-CN/checkpointing)
- [学习方法论](../learning-methodology/README.md)

---

**Last Updated**: May 31, 2026
**Claude Code Version**: 2.1.150
**Compatible Models**: Claude Sonnet 4.6, Claude Opus 4.7, Claude Haiku 4.5
```

- [ ] **Step 2: 验证文件**

```bash
grep -c "^##" my-learning/checkpoints/README.md
```

Expected: 8-10 个二级标题。

- [ ] **Step 3: Commit**

```bash
git add my-learning/checkpoints/README.md
git commit -m "docs(checkpoints): add core knowledge distilled with methodology"
```

---

### Task 5: 生成 `learning-methodology/assets/pareto-vs-occam.html`

**Files:**
- Create: `my-learning/learning-methodology/assets/pareto-vs-occam.html`

**Design:** 使用 `frontend-design` + `huashu-design` 技能生成。左右分栏动画对比：左侧演示二八法则（从一堆知识点中 20% 高亮弹出），右侧演示奥卡姆剃刀（从一段文字中逐行删除废话，留下精炼版本）。

- [ ] **Step 1: 启动视觉伴侣服务器**

```bash
# Windows — 使用 run_in_background: true
scripts/start-server.sh --project-dir d:/OpenSourceWorkSpace/claude-howto
```

> 注意：`scripts/start-server.sh` 位于 superpowers skill 目录下的 `skills/brainstorming/` 同级。查找路径：`C:\Users\lyh\.claude\plugins\cache\claude-plugins-official\superpowers\5.1.0\skills\brainstorming\scripts\start-server.sh`

获取 `screen_dir` 和 `state_dir` 从返回的 JSON。

- [ ] **Step 2: 使用 frontend-design 技能生成 HTML**

调用 `frontend-design` 技能，传入需求：

> 生成一个左右分栏的动画对比页面：
> - 左侧：二八法则演示。10 个知识点卡片散落，其中 2 个（20%）用醒目颜色高亮、放大、弹出，其余 8 个淡出。动画循环或用户触发。
> - 右侧：奥卡姆剃刀演示。一段文字逐行显示，随后"废话行"被红色划线删除，留下精炼版本。
> - 顶部标题："二八法则 vs 奥卡姆剃刀 — 一个找重点，一个砍废话"
> - 风格：简洁、专业，配色克制。避免 AI-slop 审美。

输出保存到 `my-learning/learning-methodology/assets/pareto-vs-occam.html`。

- [ ] **Step 3: 使用 huashu-design 技能复查动画质量**

调用 `huashu-design` 技能，传入步骤 2 的 HTML 进行动画润色：
- 确保过渡动画流畅（≥60fps）
- 添加恰当的缓动函数
- 确保交互反馈即时

- [ ] **Step 4: 在视觉伴侣中预览**

将生成的 HTML 复制到 `screen_dir`：
```bash
cp my-learning/learning-methodology/assets/pareto-vs-occam.html <screen_dir>/
```

在浏览器中查看效果，确认动画正常。

- [ ] **Step 5: 在 README.md 中添加引用链接**

确保 `my-learning/learning-methodology/README.md` 的 Part 4 包含：
```markdown
> [查看交互式对比演示](assets/pareto-vs-occam.html)
```

- [ ] **Step 6: Commit**

```bash
git add my-learning/learning-methodology/assets/pareto-vs-occam.html
git add my-learning/learning-methodology/README.md
git commit -m "feat(learning): add pareto vs occam visual comparison"
```

---

### Task 6: 生成 `checkpoints/assets/rewind-options.html`

**Files:**
- Create: `my-learning/checkpoints/assets/rewind-options.html`

**Design:** 交互式卡片墙。6 张卡片排列，每张代表一个回退选项。卡片显示选项名 + 一句话用途。点击卡片展开，显示详细场景模拟（动画小人或代码变化示意）。

- [ ] **Step 1: 使用 frontend-design 技能生成**

调用 `frontend-design` 技能：

> 生成一个交互式卡片墙页面，展示 Claude Code Checkpoints 的 6 个回退选项：
> 1. 恢复代码和对话 — 全回退
> 2. 恢复对话 — 只退对话
> 3. 恢复代码 — 只退代码
> 4. 从此处总结 — 压缩后续
> 5. 到此处总结 — 压缩前置
> 6. 算了 — 取消
>
> 布局：2 行 × 3 列卡片网格。每张卡片默认显示"选项名 + 一句话用途"。点击展开，显示详细说明 + 使用场景动画。
> 按使用频率从左到右排列。
> 风格：简洁专业，信息层次清晰。

保存到 `my-learning/checkpoints/assets/rewind-options.html`。

- [ ] **Step 2: huashu-design 动画润色**

调用 `huashu-design` 技能审查动画质量。

- [ ] **Step 3: 在 README.md 中添加引用链接**

确保 `my-learning/checkpoints/README.md` 的"6 个回退选项"部分包含：
```markdown
> [查看交互式选项对比](assets/rewind-options.html)
```

- [ ] **Step 4: Commit**

```bash
git add my-learning/checkpoints/assets/rewind-options.html
git add my-learning/checkpoints/README.md
git commit -m "feat(checkpoints): add rewind options interactive cards"
```

---

### Task 7: 生成 `checkpoints/assets/workflow-patterns.html`

**Files:**
- Create: `my-learning/checkpoints/assets/workflow-patterns.html`

**Design:** 4 个工作流模式的动画流程图。顶部 tab 切换 4 个模式。每个模式是 Mermaid 风格的动画路径图，节点按流程自动推进，高亮当前步骤。支持用户点击"下一步"手动推进或自动播放。

4 个模式：
1. 分支探索：Save → Try A → Rewind → Try B → Compare → Choose
2. 安全重构：Save → Refactor → Test → [Pass → Continue] / [Fail → Rewind]
3. A-B 测试：Save → Design A → Save → Rewind → Design B → Compare
4. 错误恢复：Notice Bug → Rewind → Fix

- [ ] **Step 1: 使用 frontend-design 技能生成**

调用 `frontend-design` 技能生成流程图页面。保存到 `my-learning/checkpoints/assets/workflow-patterns.html`。

- [ ] **Step 2: huashu-design 动画润色**

- [ ] **Step 3: 在 README.md 中添加引用链接**

确保包含：
```markdown
> [查看工作流动画演示](assets/workflow-patterns.html)
```

- [ ] **Step 4: Commit**

```bash
git add my-learning/checkpoints/assets/workflow-patterns.html
git add my-learning/checkpoints/README.md
git commit -m "feat(checkpoints): add workflow patterns animated diagrams"
```

---

### Task 8: 生成 `checkpoints/assets/restore-vs-summarize.html`

**Files:**
- Create: `my-learning/checkpoints/assets/restore-vs-summarize.html`

**Design:** 左右分栏对比页。左侧演示"恢复"——时间线回退，代码和/或对话回到之前的状态。右侧演示"总结"——时间线上某段内容被替换为摘要气泡，其余部分不变。两栏各有一个动画演示，直观展示两种操作的区别。

- [ ] **Step 1: 使用 frontend-design 技能生成**

调用 `frontend-design` 技能生成对比页。保存到 `my-learning/checkpoints/assets/restore-vs-summarize.html`。

- [ ] **Step 2: huashu-design 动画润色**

- [ ] **Step 3: 在 README.md 中添加引用链接**

确保"关键限制"部分包含：
```markdown
> [查看恢复 vs 总结差异对比](assets/restore-vs-summarize.html)
```

- [ ] **Step 4: Commit**

```bash
git add my-learning/checkpoints/assets/restore-vs-summarize.html
git add my-learning/checkpoints/README.md
git commit -m "feat(checkpoints): add restore vs summarize comparison"
```

---

### Task 9: 生成 `learning-methodology/assets/methodology-flow.html`

**Files:**
- Create: `my-learning/learning-methodology/assets/methodology-flow.html`

**Design:** 4 步方法论动画流程图。从上到下的流程，每步一个节点。用户可点击展开步骤查看详细说明和 Checkpoints 演示。默认自动播放完整流程（~15秒）。

- [ ] **Step 1: 使用 frontend-design 技能生成**

调用 `frontend-design` 技能。保存到 `my-learning/learning-methodology/assets/methodology-flow.html`。

- [ ] **Step 2: huashu-design 动画润色**

- [ ] **Step 3: 在 README.md 中添加引用链接**

确保"四步操作法"部分包含：
```markdown
> [查看交互式流程图](assets/methodology-flow.html)
```

- [ ] **Step 4: Commit**

```bash
git add my-learning/learning-methodology/assets/methodology-flow.html
git add my-learning/learning-methodology/README.md
git commit -m "feat(learning): add methodology flow animation"
```

---

### Task 10: 质量检查

**Files:**
- Check: `my-learning/learning-methodology/README.md`
- Check: `my-learning/learning-methodology/prompt-templates.md`
- Check: `my-learning/checkpoints/README.md`
- Check: All files in `my-learning/*/assets/`

- [ ] **Step 1: 验证所有相对链接**

```bash
# 检查 markdown 中的相对链接是否指向存在的文件
grep -oP '\[.*?\]\(\.\.?/[^)]+\)' my-learning/learning-methodology/README.md | grep -oP '(?<=\()[^)]+' | while read link; do
  dir=$(dirname my-learning/learning-methodology/README.md)
  target="$dir/$link"
  if [ ! -f "$target" ]; then echo "BROKEN: $link"; fi
done

grep -oP '\[.*?\]\(\.\.?/[^)]+\)' my-learning/checkpoints/README.md | grep -oP '(?<=\()[^)]+' | while read link; do
  dir=$(dirname my-learning/checkpoints/README.md)
  target="$dir/$link"
  if [ ! -f "$target" ]; then echo "BROKEN: $link"; fi
done
```

Expected: 无 "BROKEN" 输出。

- [ ] **Step 2: 验证内容完整性**

```bash
# 方法论文档应含 7 个部分
echo "=== Methodology README sections ==="
grep -c "^## " my-learning/learning-methodology/README.md

# Prompt templates 应含 4 个模板
echo "=== Prompt templates count ==="
grep -c "^## 模板" my-learning/learning-methodology/prompt-templates.md

# Checkpoints 应含 5+ 部分
echo "=== Checkpoints README sections ==="
grep -c "^## " my-learning/checkpoints/README.md
```

Expected: Methodology ≥7, Templates = 4, Checkpoints ≥5.

- [ ] **Step 3: 验证 Markdown 无内嵌 HTML**

```bash
# Markdown 文件不应包含 <html> 或 <style> 或 <script> 标签
grep -rln '<\(html\|style\|script\|div\|iframe\)' my-learning/*/*.md
```

Expected: 无匹配（空输出）。

- [ ] **Step 4: 验证 HTML 文件可独立打开**

```bash
# 每个 HTML 文件应有完整文档结构
for f in my-learning/*/assets/*.html; do
  if grep -q '<!DOCTYPE html>' "$f" || grep -q '<html' "$f"; then
    echo "OK: $f"
  else
    echo "MISSING STRUCTURE: $f"
  fi
done
```

Expected: 全部 "OK"。

- [ ] **Step 5: 修复发现的问题并 Commit**

```bash
git add -A my-learning/
git commit -m "chore(learning): quality check and fix broken links"
```

---

### Task 11: 最终提交

- [ ] **Step 1: 确认所有文件已提交**

```bash
git status
```

Expected: 无未提交文件。

- [ ] **Step 2: 推送**

```bash
# 注意：仅在用户明确要求时推送
echo "Ready to push. Waiting for user confirmation."
```
