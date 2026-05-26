# 实现计划：学习打卡 Issue 创建工具

## 概述

根据设计规格文档，创建一个可复用的 Python 脚本和配套的模块数据文件。

## 交付物

| #    | 文件                                | 说明                |
| ---- | ----------------------------------- | ------------------- |
| 1    | `scripts/learning_modules.yaml`     | 10 个模块的数据定义 |
| 2    | `scripts/create_learning_issues.py` | 主脚本              |

## 步骤

### 步骤 1：创建模块数据文件

**文件**：`scripts/learning_modules.yaml`

按学习路径顺序定义 10 个模块：

```yaml
modules:
  - order: 1
    title: "Slash Commands"
    folder: "01-slash-commands"
    level: "beginner"
    time: "30 min"
    doc_link: "https://docs.anthropic.com/en/docs/claude-code/slash-commands"
  - order: 2
    title: "Memory"
    folder: "02-memory"
    level: "beginner+"
    time: "45 min"
    doc_link: "https://docs.anthropic.com/en/docs/claude-code/memory"
  - order: 3
    title: "Checkpoints"
    folder: "08-checkpoints"
    level: "intermediate"
    time: "45 min"
    doc_link: "https://docs.anthropic.com/en/docs/claude-code/checkpoints"
  - order: 4
    title: "CLI Reference"
    folder: "10-cli"
    level: "beginner+"
    time: "30 min"
    doc_link: "https://docs.anthropic.com/en/docs/claude-code/cli-reference"
  - order: 5
    title: "Skills"
    folder: "03-skills"
    level: "intermediate"
    time: "1 hour"
    doc_link: "https://docs.anthropic.com/en/docs/claude-code/skills"
  - order: 6
    title: "Hooks"
    folder: "06-hooks"
    level: "intermediate"
    time: "1 hour"
    doc_link: "https://docs.anthropic.com/en/docs/claude-code/hooks"
  - order: 7
    title: "MCP"
    folder: "05-mcp"
    level: "intermediate+"
    time: "1 hour"
    doc_link: "https://docs.anthropic.com/en/docs/claude-code/mcp"
  - order: 8
    title: "Subagents"
    folder: "04-subagents"
    level: "intermediate+"
    time: "1.5 hours"
    doc_link: "https://docs.anthropic.com/en/docs/claude-code/subagents"
  - order: 9
    title: "Advanced Features"
    folder: "09-advanced-features"
    level: "advanced"
    time: "2-3 hours"
    doc_link: "https://docs.anthropic.com/en/docs/claude-code/advanced-features"
  - order: 10
    title: "Plugins"
    folder: "07-plugins"
    level: "advanced"
    time: "2 hours"
    doc_link: "https://docs.anthropic.com/en/docs/claude-code/plugins"
```

**验证**：YAML 语法正确，10 个条目，order 连续。

---

### 步骤 2：创建 Python 脚本

**文件**：`scripts/create_learning_issues.py`

**依赖**：仅标准库（`argparse`、`subprocess`、`yaml` 需 `pip install pyyaml`，项目已有）

**脚本结构**：

```
main()
├── parse_args()              # 解析 CLI 参数
├── verify_gh()               # 验证 gh 已安装且已登录
├── load_modules(path)        # 读取 YAML 模块数据
├── ensure_labels(repo)       # 创建缺失标签
├── create_issues(repo, modules) → list[dict]  # 逐个创建 Issue
│   └── render_issue_body(module) → str         # 渲染模板正文
├── add_to_board(project_id, issues)  # 关联看板
└── print_summary(issues)     # 打印汇总表格
```

**参数定义**：

```python
parser.add_argument("--repo", required=True, help="目标仓库，格式：owner/repo")
parser.add_argument("--project", type=int, help="GitHub Project 编号（不传则创建新看板）")
parser.add_argument("--modules-yaml", default="scripts/learning_modules.yaml", help="模块数据文件路径")
parser.add_argument("--dry-run", action="store_true", help="仅打印将创建的内容，不实际执行")
```

**各函数职责**：

#### `verify_gh()`
- 运行 `gh auth status`，非零退出码则打印提示并退出。

#### `load_modules(path)`
- 读取 YAML，校验每个条目含 order/title/folder/level/time。
- level 必须在允许的 5 个值中。

#### `ensure_labels(repo)`
- `gh label list -R {repo} --json name` 获取已有标签名列表。
- 遍历 6 个预定义标签，缺失则 `gh label create`。
- 返回已存在的标签名集合（用于后续 Issue 创建时校验）。

#### `render_issue_body(module)`
- 填充模板，doc_link 为空时用 `（待补充）`。

#### `create_issues(repo, modules)`
- 遍历模块列表，对每个调用 `gh issue create -R {repo} --title "..." --body "..." --label "learning" --label "{level}"`。
- 捕获异常，失败不中断，记录到 results 列表。
- 解析 `gh issue create` 输出获取 Issue URL。
- 返回 `list[dict]`，每个 dict 含 order/title/folder/level/time/url/status。

#### `add_to_board(project_id, issues)`
- 若未传 project_id，则 `gh project create` 创建新看板并获取 ID。
- `gh project view {id}` 验证看板存在。
- 对每个成功创建的 Issue，`gh project item-add {id} --url {issue_url}`。

#### `print_summary(issues)`
- 用 tabulate 或手动格式化打印汇总表格。
- 标注失败条目。

**`--dry-run` 模式**：
- 不执行任何 `gh` 写操作。
- 打印将要创建的标签列表和 Issue 标题/正文预览。

---

### 步骤 3：验证

1. 运行 `python scripts/create_learning_issues.py --repo DoubleW2w/claude-howto --project 1 --dry-run`，确认输出正确。
2. 去掉 `--dry-run`，实际执行创建。
3. 检查 GitHub 上 Issue、标签、看板是否符合预期。

## 不在范围内

- 自动从源仓库 README 解析模块列表（可后续扩展）。
- Issue 完成后的自动归档/通知。
- 与现有测试框架的集成测试。
