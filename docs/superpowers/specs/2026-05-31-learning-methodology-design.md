---
name: learning-methodology-design
description: 二八法则+奥卡姆剃刀学习方法论 + Checkpoints核心知识 设计规格
---

# 学习方法论 + Checkpoints 核心知识 设计规格

## 背景

用户在学习 claude-howto 教程仓库。希望建立一套可复用的快速学习方法论（二八法则+奥卡姆剃刀），同时用 Checkpoints 作为第一个实践案例，产出一份精简的核心知识文档。

方法论用于后续学习仓库其他模块时复用。

## 核心决策

**方案 B：两份独立 Markdown + 精美 HTML 可视化（frontend-design + huashu-design）**

HTML 文件不是固定 2 个，而是按知识点需求驱动——哪些概念用动画/交互展示更直观，就生成对应 HTML。所有 HTML 使用 `frontend-design` 或者 `huashu-design` 技能制作，目的是使用它们的规范，确保设计质量和动画效果，而不是为了精美而精美，选择哪个技能，选择权在于你，但要统一风格。

方法论和 Checkpoints 相互独立可读，方法论以 Checkpoints 为完整演示案例。

## 目录结构

```
my-learning/
├── learning-methodology/
│   ├── README.md                   # 方法论正文（原理+步骤+演示+陷阱+边界）
│   ├── prompt-templates.md         # 4个可复用 Prompt 模板
│   └── assets/                     # 按需生成 HTML 视觉文件
└── checkpoints/
    ├── README.md                   # Checkpoints 核心知识（精简版）
    └── assets/                     # 按需生成 HTML 视觉文件
```

## 文件规格

### 1. `learning-methodology/README.md`

**7个部分，总量约 1500 字：**

1. **核心理念**（200字）
   - 二八法则：20% 输入 → 80% 输出
   - 奥卡姆剃刀：如无必要，勿增实体
   - 两句讲清组合：一个找重点，一个砍废话

2. **四步操作法**（300字）
   - 第一步：定位信息源 → 官方文档 + 优质教程
   - 第二步：抓取骨骼 → 目录/标题/关键词表/API列表（不要内容）
   - 第三步：提取核心 → 用二八法则筛出 4-6 个关键点
   - 第四步：去噪成文 → 用奥卡姆剃刀砍掉解释性废话、重复例子，留最小可运行知识
   - 终止条件：如果资料已足够精炼，不再强行压缩

3. **完整演示：Checkpoints**（500字）
   - 信息源：`08-checkpoints/README.md` + 官方文档 `code.claude.com/docs/zh-CN/checkpointing`
   - 骨骼：6个回退选项、3个入口方式、4个场景、3个限制
   - 核心：砍掉自动机制细节、配置细节、故障排查 → 留核心概念
   - 成文：最终 Checkpoints README 怎么组织的

4. **核心概念卡**（300字，配 HTML 链接）
   - 二八法则卡：适用场景、操作要诀、判断标准
   - 奥卡姆剃刀卡：何时用、何时不用、常见误用

5. **常见陷阱**（200字）
   - 过度精简：砍掉必要的上下文
   - 伪核心：把"目录"当"核心"
   - 一成不变：不同领域 20% 长得不一样
   - 边际价值降低：已精炼的内容不再强行压缩

6. **适用边界**（150字）
   - 不适合：医学、法律等需要精确完整的领域
   - 最适合：工具类、框架类、概念类知识

7. **Prompt 模板入口**
   - 链接到 `prompt-templates.md`

### 2. `learning-methodology/prompt-templates.md`

**4个模板，每个独立可复制：**

| 模板 | 用途 | 对应步骤 |
|------|------|---------|
| 骨骼提取 | 提取目录/概念/API表，不要正文 | 第二步 |
| 核心提炼 | 用二八法则筛出 ≤6 张核心概念卡 | 第三步 |
| 去噪精简 | 砍重复解释、教条废话、冗余示例 | 第四步 |
| 快速入门 | 组合上述三步，从零掌握新领域 | 全流程 |

每个模板包含：适用场景一句话、完整 Prompt 文本、用 Checkpoints 做的示例输出。

### 3. `checkpoints/README.md`

**5个部分，总量约 600 字：**

1. **一句话定义**（50字）
2. **核心概念 3 张卡**：Checkpoint / Rewind / Summarize（200字）
3. **入口**：Esc+Esc 或 /rewind 或 /checkpoint（50字）
4. **6个选项速查表**（200字）：选项名 / 做什么 / 什么时候用
5. **三要三不要**（100字）

不重复 `08-checkpoints/README.md` 已有的冗余内容，用交叉引用链接回原文。

## HTML 视觉文件规格

### 生成原则

- 不预先定死个数和文件名
- 由知识点需求驱动：某个概念用动画/交互展示更直观 → 生成 HTML
- 所有 HTML 使用 `frontend-design` 技能控制设计质量，避免 AI-slop 审美
- 所有 HTML 使用 `huashu-design` 技能添加动画、交互、视觉层次
- HTML 文件自包含，浏览器直接打开
- Markdown 通过相对链接引用：`[查看交互演示](assets/xxx.html)`
- 视觉伴侣服务器托管 `assets/` 目录，实时预览

### 候选视觉点

| 知识点 | 视觉形式 | 为什么 |
|--------|---------|--------|
| 4步方法论流程 | 动画流程图，步骤逐一出场 | 文字步骤易跳读，动画建立心智模型 |
| 二八法则 vs 奥卡姆剃刀 | 左右分栏动画对比 | 两概念易混淆，并列对比区分 |
| 6个回退选项 | 交互式卡片墙，点击展开场景模拟 | 信息密度高，边看边决策更直观 |
| 4个工作流模式 | 动画流程图，节点状态切换 | 分支/回退是空间逻辑，纯文字难传达 |
| 恢复 vs 总结差异 | 左右分栏，区域高亮影响范围 | 两概念易混淆，对比图清晰 |

### 设计质量要求

- `frontend-design`：产出有辨识度的设计，避免通用 AI 风格
- `huashu-design`：动画过渡自然，交互反馈即时，视觉层次分明

## 约束

- Markdown 不含 HTML 代码块，保持纯文本干净
- 所有链接使用相对路径
- 遵循项目 STYLE_GUIDE.md 和 CLAUDE.md 规范
- 不修改 `08-checkpoints/` 原有内容

## 实现阶段

1. 启动视觉伴侣服务器
2. 编写 `learning-methodology/README.md`
3. 编写 `learning-methodology/prompt-templates.md`
4. 编写 `checkpoints/README.md`
5. 按需逐个生成 HTML 视觉文件（frontend-design + huashu-design）
6. 质量检查：链接有效性、内容一致性
