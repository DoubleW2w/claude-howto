# 学习打卡 Issue 创建工具 — 设计规格

## 目标

创建一个可复用的 Python 脚本，用于在 GitHub 上生成标准化的学习打卡 Issue，自动添加标签并关联到项目看板，最后打印汇总表格。本工具为 claude-howto 教程仓库设计，但适用于任意仓库。

## 用法

```bash
python scripts/create_learning_issues.py \
  --repo DoubleW2w/claude-howto \
  --project 1 \
  --modules-yaml modules.yaml
```

## 输入：模块数据（YAML）

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
    doc_link: ""
  # ...
```

- `doc_link` 可选，为空时显示 `（待补充）`。
- `level` 取值范围：`beginner`、`beginner+`、`intermediate`、`intermediate+`、`advanced`。

## 标签管理

脚本管理 6 个标签。通过 `gh label list` 查询已有标签，仅创建缺失的。

| 标签 | 颜色 | 说明 |
|------|------|------|
| `learning` | `#0075CA` | 学习打卡任务 |
| `beginner` | `#4CAF50` | 入门级 |
| `beginner+` | `#8BC34A` | 进阶入门 |
| `intermediate` | `#FFC107` | 中级 |
| `intermediate+` | `#FF9800` | 进阶中级 |
| `advanced` | `#F44336` | 高级 |

每个 Issue 打 2 个标签：`learning` + 对应难度级别。

## Issue 模板

**标题**：`[Module {order}] {title}`

**正文**（5 个板块）：

```
## 📚 学习材料与阅读
- 📂 模块文件夹：`{folder}/`
- 📝 对应官方文档：{doc_link or （待补充）}
- [ ] 精读 README.md，理解核心概念与关键术语
- [ ] 浏览模块内所有模板文件和示例代码
- [ ] 阅读关联的官方文档链接

## 🛠️ 上手实操
- [ ] 将模板文件复制到自己的测试项目中
- [ ] 实际运行并验证效果
- [ ] 记录遇到的问题和解决方案

## 🚀 自由构建
- [ ] 基于该模块功能，设计一个自己的使用场景
- [ ] 编写自定义配置/脚本

## ✅ 自我测评
- [ ] 运行 `/lesson-quiz` 对应主题，检查掌握程度
- [ ] 回顾学习目标，确认是否达成

## 📝 学习笔记
> 在此记录你的学习心得、踩坑记录和关键收获...
```

## 看板关联

1. 通过 `gh project view {id}` 验证看板是否存在。
2. 不存在则通过 `gh project create --title "学习看板"` 创建。
3. 通过 `gh project item-add` 将每个 Issue 添加到看板。默认状态为 "Todo"，无需额外操作。

## 汇总输出

完成后打印表格：

```
| # | 标题                     | 模块文件夹            | 预计用时 | 难度          | Issue 链接 |
|---|--------------------------|-----------------------|----------|---------------|------------|
| 1 | [Module 1] Slash Commands| 01-slash-commands/    | 30 min   | beginner      | ...        |
| ...                                                                                           |

📊 共创建 X 个 Issue，已关联到看板 #N
🏷️  标签：learning, beginner, beginner+, intermediate, intermediate+, advanced
```

## 执行流程

```
解析参数 → 验证 gh CLI → 读取模块 YAML → 创建标签 → 逐个创建 Issue → 关联看板 → 打印汇总
```

## 错误处理

- `gh` 未安装或未登录 → 退出并给出明确提示。
- 单条 Issue 创建失败 → 记录错误，继续处理剩余 Issue。
- 汇总中标注失败的条目。

## 约束

- 所有 GitHub 操作通过 `gh` CLI 完成（不使用 PyGithub 或 REST API）。
- 脚本位于 `scripts/create_learning_issues.py`。
- 模块数据默认路径 `scripts/learning_modules.yaml`（可通过 `--modules-yaml` 覆盖）。
