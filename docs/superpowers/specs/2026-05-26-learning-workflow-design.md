---
name: learning-workflow-design
description: Fork + independent branch learning workflow design for claude-howto
---

# 学习笔记工作流设计

## 背景

fork 仓库 `DoubleW2w/claude-howto`，上游为 `luongnv89/claude-howto`（无 push 权限）。需要在学习教程的同时记录实践笔记、踩坑过程、整合重点知识，形成独立的学习笔记体系，公开分享给社区。

## 核心决策

**方案：fork + 独立分支**

放弃独立仓库方案，原因：Claude Code 绑定工作目录，独立仓库需要来回切换，且无法同时索引教程原文和笔记代码。

放弃多分支方案，原因：学习是累积的，多分支切断上下文引用，管理成本高。

## 分支策略

| 分支 | 用途 | 同步方式 |
|------|------|----------|
| `main` | 保持与 upstream 同步，不做任何修改 | 定期 `merge upstream/main` |
| `notes/lyhovo` | 日常工作分支，包含教程原文 + 笔记/实践代码 | 从 `main` merge 获取上游更新 |

## 目录结构

```
notes/lyhovo 分支根目录
├── 01-slash-commands/       ← 教程原文（继承自 main）
├── ...                      ← 教程原文
├── 10-mcp/                  ← 教程原文
├── my-learning/             ← 学习内容（按主题自由组织）
│   ├── slash-commands/
│   │   ├── notes.md         ← 实践笔记、踩坑记录
│   │   └── practice/        ← 可运行代码
│   ├── hooks/
│   │   ├── notes.md
│   │   └── practice/
│   └── ...
├── docs/superpowers/        ← superpowers skill 输出（设计文档、计划等）
├── scripts/                 ← 教程原有脚本
└── README.md                ← 教程原有 README
```

`my-learning/` 下按自己理解的主题归类，不跟随 `01-`~`10-` 编号。

`docs/superpowers/` 保留原位，不迁入 `my-learning/`。这是 superpowers skill 的输出目录，未来继续使用 skill 时会往这里写文件。

## 同步上游流程

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
git checkout notes/lyhovo
git merge main              # my-learning/ 在 main 中不存在，零冲突
git push origin notes/lyhovo
```

## 进度管理

使用 GitHub Projects 看板 + issue 跟踪学习进度，与分支无关。

## .gitignore 处理

`my-learning/` 下的实践代码可能产生临时文件（`node_modules/`、`__pycache__/`、`.env` 等），在 `notes/lyhovo` 分支上补充 `.gitignore` 规则，不影响 `main`。

## 初始化步骤

```bash
git checkout -b notes/lyhovo    # 从 main 创建
mkdir my-learning               # 创建笔记根目录
```
