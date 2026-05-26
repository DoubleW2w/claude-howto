#!/usr/bin/env python3
"""Create standardized learning-checkin Issues on GitHub from a YAML module list."""

import argparse
import io
import json
import subprocess
import sys
from pathlib import Path

# Windows 控制台 UTF-8 输出
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import yaml

LABELS = {
    "learning":      {"color": "0075CA", "desc": "学习打卡任务"},
    "beginner":      {"color": "4CAF50", "desc": "入门级"},
    "beginner+":     {"color": "8BC34A", "desc": "进阶入门"},
    "intermediate":  {"color": "FFC107", "desc": "中级"},
    "intermediate+": {"color": "FF9800", "desc": "进阶中级"},
    "advanced":      {"color": "F44336", "desc": "高级"},
}

VALID_LEVELS = {"beginner", "beginner+", "intermediate", "intermediate+", "advanced"}

ISSUE_BODY_TEMPLATE = """\
## 📚 学习材料与阅读
- 📂 模块文件夹：`{folder}/`
- 📝 对应官方文档：{doc_link}
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
> 在此记录你的学习心得、踩坑记录和关键收获..."""


def run_gh(*args: str, capture: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["gh", *args],
        capture_output=capture,
        text=True,
        encoding="utf-8",
    )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="创建学习打卡 Issue 并关联到 GitHub Project 看板",
    )
    parser.add_argument(
        "--repo", required=True,
        help="目标仓库，格式：owner/repo",
    )
    parser.add_argument(
        "--project", type=int,
        help="GitHub Project 编号（不传则创建新看板）",
    )
    parser.add_argument(
        "--modules-yaml",
        default=str(Path(__file__).parent / "learning_modules.yaml"),
        help="模块数据文件路径",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="仅打印将创建的内容，不实际执行",
    )
    return parser.parse_args()


def verify_gh() -> None:
    result = run_gh("auth", "status")
    if result.returncode != 0:
        print("❌ gh CLI 未安装或未登录。请先运行：")
        print("   gh auth login")
        sys.exit(1)


def load_modules(path: str) -> list[dict]:
    p = Path(path)
    if not p.exists():
        print(f"❌ 模块数据文件不存在：{path}")
        sys.exit(1)

    with open(p, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    modules = data.get("modules", [])
    required_keys = {"order", "title", "folder", "level", "time"}
    for i, m in enumerate(modules):
        missing = required_keys - m.keys()
        if missing:
            print(f"❌ 第 {i + 1} 个模块缺少字段：{missing}")
            sys.exit(1)
        if m["level"] not in VALID_LEVELS:
            print(f"❌ 第 {i + 1} 个模块 level 无效：{m['level']}")
            sys.exit(1)

    return modules


def ensure_labels(repo: str, dry_run: bool) -> None:
    if dry_run:
        print("\n🏷️  将创建以下标签（如不存在）：")
        for name, cfg in LABELS.items():
            print(f"   {name} (#{cfg['color']}) - {cfg['desc']}")
        return

    result = run_gh("label", "list", "-R", repo, "--json", "name")
    if result.returncode != 0:
        print(f"❌ 获取标签列表失败：{result.stderr}")
        sys.exit(1)

    existing = {item["name"] for item in json.loads(result.stdout)}

    for name, cfg in LABELS.items():
        if name in existing:
            print(f"   ⏭️  标签已存在：{name}")
            continue
        r = run_gh(
            "label", "create", name,
            "-R", repo,
            "--color", cfg["color"],
            "--description", cfg["desc"],
        )
        if r.returncode == 0:
            print(f"   ✅ 已创建标签：{name}")
        else:
            print(f"   ⚠️  创建标签失败：{name} — {r.stderr.strip()}")


def render_issue_body(module: dict) -> str:
    doc_link = module.get("doc_link") or "（待补充）"
    return ISSUE_BODY_TEMPLATE.format(
        folder=module["folder"],
        doc_link=doc_link,
    )


def create_issues(repo: str, modules: list[dict], dry_run: bool) -> list[dict]:
    results = []

    for m in modules:
        title = f"[Module {m['order']}] {m['title']}"
        body = render_issue_body(m)
        level = m["level"]

        entry = {
            "order": m["order"],
            "title": title,
            "folder": m["folder"],
            "level": level,
            "time": m["time"],
            "url": "",
            "status": "pending",
        }

        if dry_run:
            print(f"\n📌 Issue #{m['order']}: {title}")
            print(f"   标签：learning, {level}")
            print(f"   正文预览（前 120 字）：{body[:120]}...")
            entry["status"] = "dry-run"
            results.append(entry)
            continue

        r = run_gh(
            "issue", "create",
            "-R", repo,
            "--title", title,
            "--body", body,
            "--label", "learning",
            "--label", level,
        )

        if r.returncode == 0:
            url = r.stdout.strip()
            entry["url"] = url
            entry["status"] = "created"
            print(f"   ✅ Issue 已创建：{title}")
            print(f"      {url}")
        else:
            entry["status"] = "failed"
            print(f"   ❌ Issue 创建失败：{title}")
            print(f"      {r.stderr.strip()}")

        results.append(entry)

    return results


def _get_owner(repo: str) -> str:
    return repo.split("/")[0]


def resolve_project(project_id: int | None, repo: str, dry_run: bool) -> int | None:
    owner = _get_owner(repo)

    if dry_run:
        if project_id:
            print(f"\n📋 将使用看板 #{project_id} (owner: {owner})")
        else:
            print("\n📋 将创建新看板")
        return project_id

    if project_id is None:
        r = run_gh("project", "create", "--title", "学习看板", "--owner", owner, "--format", "json")
        if r.returncode != 0:
            print(f"❌ 创建看板失败：{r.stderr}")
            return None
        data = json.loads(r.stdout)
        project_id = data.get("number") or data.get("id")
        print(f"📋 已创建新看板 #{project_id}")
        return project_id

    r = run_gh("project", "view", str(project_id), "--owner", owner, "--format", "json")
    if r.returncode != 0:
        print(f"❌ 看板 #{project_id} 不存在或无权访问：{r.stderr}")
        return None

    print(f"📋 已确认看板 #{project_id}")
    return project_id


def add_to_board(project_id: int | None, issues: list[dict], repo: str, dry_run: bool) -> None:
    if not project_id:
        return

    owner = _get_owner(repo)
    created = [i for i in issues if i["status"] == ("dry-run" if dry_run else "created")]
    if not created:
        print("   ⚠️  没有成功的 Issue 可关联到看板")
        return

    if dry_run:
        print(f"\n📋 将 {len(created)} 个 Issue 关联到看板 #{project_id}")
        return

    for issue in created:
        r = run_gh(
            "project", "item-add", str(project_id),
            "--owner", owner,
            "--url", issue["url"],
        )
        if r.returncode == 0:
            print(f"   ✅ 已关联到看板：{issue['title']}")
        else:
            print(f"   ⚠️  关联失败：{issue['title']} — {r.stderr.strip()}")


def print_summary(issues: list[dict]) -> None:
    print("\n" + "=" * 80)
    print("📊 创建汇总")
    print("=" * 80)

    col_widths = [4, 36, 24, 10, 16, 50]
    header = ["#", "标题", "模块文件夹", "预计用时", "难度", "Issue 链接"]
    print(f"| {header[0]:<{col_widths[0]}} | {header[1]:<{col_widths[1]}} | {header[2]:<{col_widths[2]}} | {header[3]:<{col_widths[3]}} | {header[4]:<{col_widths[4]}} | {header[5]:<{col_widths[5]}} |")
    sep = "|-" + "-+-".join("-" * w for w in col_widths) + "-|"
    print(sep)

    for i in issues:
        title = i["title"][:col_widths[1] - 2]
        folder = i["folder"][:col_widths[2] - 2]
        level = i["level"][:col_widths[4] - 2]
        url = i.get("url", "")[:col_widths[5] - 2]
        if i["status"] == "failed":
            url = "❌ 创建失败"

        print(f"| {i['order']:<{col_widths[0]}} | {title:<{col_widths[1]}} | {folder:<{col_widths[2]}} | {i['time']:<{col_widths[3]}} | {level:<{col_widths[4]}} | {url:<{col_widths[5]}} |")

    created_count = sum(1 for i in issues if i["status"] in ("created", "dry-run"))
    failed_count = sum(1 for i in issues if i["status"] == "failed")
    print()
    print(f"📊 共 {created_count} 个 Issue 创建成功" + (f"，{failed_count} 个失败" if failed_count else ""))
    print(f"🏷️  标签：{', '.join(LABELS.keys())}")


def main() -> None:
    args = parse_args()

    if args.dry_run:
        print("🔍 DRY RUN 模式 — 不执行实际操作\n")

    verify_gh()

    print(f"📂 目标仓库：{args.repo}")
    print(f"📄 模块数据：{args.modules_yaml}")

    modules = load_modules(args.modules_yaml)
    print(f"✅ 已加载 {len(modules)} 个模块")

    print("\n🏷️  标签管理")
    ensure_labels(args.repo, args.dry_run)

    print("\n📝 创建 Issue")
    issues = create_issues(args.repo, modules, args.dry_run)

    print("\n📋 看板关联")
    project_id = resolve_project(args.project, args.repo, args.dry_run)
    add_to_board(project_id, issues, args.repo, args.dry_run)

    print_summary(issues)


if __name__ == "__main__":
    main()
