# Learning Branch 初始化计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 fork 仓库中创建 `notes/lyhovo` 分支，初始化 `my-learning/` 目录结构和 `.gitignore` 规则，建立日常学习工作流。

**Architecture:** `notes/lyhovo` 分支从 `main` 创建，包含全部教程原文 + 新增的 `my-learning/` 目录。`main` 保持干净用于上游同步。两个分支通过定期 merge 同步。

**Tech Stack:** Git, Markdown

---

### Task 1: 创建 notes/lyhovo 分支

**Files:**
- N/A（git 操作）

- [ ] **Step 1: 确认当前在 main 且与 upstream 同步**

```bash
git checkout main
git fetch upstream
git log --oneline main..upstream/main | wc -l
```

Expected: 输出 `0`（表示无落后）。如果不为 0，先执行 `git merge upstream/main`。

- [ ] **Step 2: 创建 notes/lyhovo 分支**

```bash
git checkout -b notes/lyhovo
```

Expected: 切换到 `notes/lyhovo` 分支，内容与 `main` 完全一致。

- [ ] **Step 3: 推送到 origin**

```bash
git push -u origin notes/lyhovo
```

Expected: 远程创建 `notes/lyhovo` 分支并设置跟踪。

---

### Task 2: 迁移已有的学习脚本

当前 `main` 上有 2 个未跟踪的学习相关脚本需要带到 `notes/lyhovo` 分支：

- `scripts/create_learning_issues.py`
- `scripts/learning_modules.yaml`

`docs/superpowers/` 保留原位不迁移（superpowers skill 的输出目录）。

**Files:**
- Move: `scripts/create_learning_issues.py` → `my-learning/scripts/create_learning_issues.py`
- Move: `scripts/learning_modules.yaml` → `my-learning/scripts/learning_modules.yaml`

- [ ] **Step 1: 创建 my-learning/ 目录结构**

```bash
mkdir -p my-learning/scripts
```

- [ ] **Step 2: 迁移学习脚本**

```bash
mv scripts/create_learning_issues.py my-learning/scripts/
mv scripts/learning_modules.yaml my-learning/scripts/
```

- [ ] **Step 3: 确认迁移结果**

```bash
git status
```

Expected: `my-learning/` 下的文件显示为 untracked，`scripts/create_learning_issues.py` 等原位置文件消失。

---

### Task 3: 创建 my-learning/README.md

**Files:**
- Create: `my-learning/README.md`

- [ ] **Step 1: 编写 README**

```markdown
# My Learning Notes

Claude Code 教程学习笔记与实验记录。

## 结构

- `slash-commands/` — 模块 1 学习笔记与实践
- `hooks/` — 模块 2 学习笔记与实践
- `scripts/` — 辅助脚本（issue 创建等）

## 与上游关系

- `main` 分支：与 [luongnv89/claude-howto](https://github.com/luongnv89/claude-howto) 保持同步
- `notes/lyhovo` 分支：日常工作分支，包含教程原文 + 本目录下的学习内容
```

---

### Task 4: 补充 .gitignore 规则

在现有 `.gitignore` 末尾追加 `my-learning/` 下实践代码可能产生的临时文件规则。

**Files:**
- Modify: `.gitignore`（追加规则）

- [ ] **Step 1: 在 .gitignore 末尾追加学习分支专用规则**

追加内容：

```gitignore
# my-learning practice code artifacts
my-learning/**/node_modules/
my-learning/**/.venv/
my-learning/**/__pycache__/
my-learning/**/.env
my-learning/**/.env.local
```

- [ ] **Step 2: 验证规则生效**

```bash
# 创建一个临时测试文件
mkdir -p my-learning/test-practice
touch my-learning/test-practice/node_modules
git status my-learning/test-practice/node_modules
# 清理
rm -rf my-learning/test-practice
```

Expected: `node_modules` 文件不出现在 git status 中。

---

### Task 5: 首次提交并推送

**Files:**
- N/A（git 操作）

- [ ] **Step 1: 查看待提交内容**

```bash
git status
git diff .gitignore
```

确认：
- `.gitignore` 追加了学习分支规则
- `my-learning/` 下有 README、scripts

- [ ] **Step 2: 提交**

```bash
git add .gitignore my-learning/
git commit -m "feat(learning): initialize notes/lyhovo branch with my-learning/ directory"
```

- [ ] **Step 3: 推送**

```bash
git push origin notes/lyhovo
```

Expected: `notes/lyhovo` 分支推送到远程，包含所有初始化内容。

- [ ] **Step 4: 验证 main 分支干净**

```bash
git checkout main
git status
git log --oneline -1
```

Expected: `main` 分支无变化，最新 commit 仍是上游同步的 commit。

```bash
git checkout notes/lyhovo
```

切回 `notes/lyhovo` 分支继续日常工作。

---

### Task 6: 设置 GitHub 默认分支（手动）

在 GitHub 仓库 `DoubleW2w/claude-howto` 设置中将默认分支改为 `notes/lyhovo`，这样：

- 访问仓库时首先看到学习内容
- PR 和 issue 默认基于 `notes/lyhovo` 分支

**操作步骤：**

1. 打开 `https://github.com/DoubleW2w/claude-howto/settings/branches`
2. Default branch → 切换为 `notes/lyhovo`
3. 确认

> 注意：这是手动操作，不通过脚本执行。可根据个人偏好决定是否修改。
