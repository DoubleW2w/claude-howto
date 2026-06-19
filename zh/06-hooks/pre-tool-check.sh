#!/bin/bash
# Bash 命令的 pre-tool 安全检查
# Hook: PreToolUse（matcher: Bash）
#
# 本 hook 在每次 Bash 工具执行前运行，阻断或警告可能具有破坏性
# 或高风险的 shell 命令。
#
# 安装：
#   cp 06-hooks/pre-tool-check.sh ~/.claude/hooks/
#   chmod +x ~/.claude/hooks/pre-tool-check.sh
#
# 在 ~/.claude/settings.json 中配置：
#   {
#     "hooks": {
#       "PreToolUse": [
#         {
#           "matcher": "Bash",
#           "hooks": [
#             {
#               "type": "command",
#               "command": "~/.claude/hooks/pre-tool-check.sh"
#             }
#           ]
#         }
#       ]
#     }
#   }
#
# 输入：通过 stdin 的 JSON，结构为：
#   { "tool_name": "Bash", "tool_input": { "command": "..." } }
#
# 输出约定（遵循 Claude Code hook 协议）：
#   - exit 0 → 允许。stdout 可包含 JSON（hookSpecificOutput）；stderr
#     会被静默丢弃，因此打印到 stderr 的警告不可见。
#     若要对已允许的命令留痕，写入审计日志文件。
#   - exit 2 → 阻断。stderr 会作为阻断理由返回给 Claude。
#     任何解释命令*为何*被阻断的 echo 都必须用 `>&2` 重定向到
#     stderr，否则 Claude Code 会报 "No stderr output"。
#
# 审计日志：每次调用都记录到
#   $CLAUDE_PROJECT_DIR/.claude/hooks/audit.log
# 含决策（BLOCK/WARN/ALLOW），这样即使 WARN 层的 stderr 输出被
# Claude Code 丢弃，你仍能观察到这些匹配。

# 从 stdin 读取完整 JSON 输入
INPUT=$(cat)

# 用可移植的 sed 提取命令（兼容 macOS 和 Linux）
COMMAND=$(echo "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

# 提取失败则回退到原始输入
if [ -z "$COMMAND" ]; then
  COMMAND="$INPUT"
fi

# ── 审计日志 ─────────────────────────────────────────────────────────────────
# 用最终决策记录每次调用。这是观察 WARN 层的唯一可靠方式，
# 因为 Claude Code 在 exit 0 时会静默丢弃 stderr。当 hook 在
# Claude Code 之外被调用时（例如本地测试）回退到 $(pwd)。
LOG_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}/.claude/hooks"
LOG_FILE="$LOG_DIR/audit.log"
mkdir -p "$LOG_DIR" 2>/dev/null
log_decision() {
  echo "$(date -u +%FT%TZ) [$1] $COMMAND" >> "$LOG_FILE"
}

# ── 阻断模式 ──────────────────────────────────────────────────────────────────
# 这些命令被无条件阻断，因为在自动化语境下它们几乎总是破坏性的，
# 且极少是有意为之。

BLOCKED_PATTERNS=(
  # 锚定 `rm -rf /`，要求 `/` 后紧跟空白或行尾，
  # 否则子串匹配会误报，例如 `rm -rf /tmp/foo`。
  "rm -rf /([[:space:]]|$)"
  "rm -rf \*"
  "dd if=/dev/zero"
  "dd if=/dev/random"
  ":\(\)\{:\|:&\};:"  # Fork bomb（正则元字符已转义）
  "mkfs\."           # 文件系统格式化
  "format c:"        # Windows 磁盘格式化
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    log_decision "BLOCK:$pattern"
    # 这些 echo 必须输出到 stderr——Claude Code 在 exit 2 时把
    # stderr 作为阻断理由展示。写到 stdout 会显示 "No stderr output"。
    echo "❌ 已阻断：检测到可能破坏性的命令：$pattern" >&2
    echo "   命令：$COMMAND" >&2
    exit 2
  fi
done

# ── 警告模式 ──────────────────────────────────────────────────────────────────
# 这些模式有风险但可能是有意为之。记录警告并允许。

WARNING_PATTERNS=(
  "rm -rf"
  "git push --force"
  "git reset --hard"
  "git clean -f"
  "chmod -R 777"
  "sudo rm"
  "DROP TABLE"
  "DROP DATABASE"
  "truncate"
)

MATCHED_WARNINGS=""
for pattern in "${WARNING_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qi "$pattern"; then
    MATCHED_WARNINGS="${MATCHED_WARNINGS:+$MATCHED_WARNINGS,}$pattern"
    # 在 stderr 上为手动运行 hook 的人镜像警告。
    # Claude Code 在 exit 0 时会丢弃它——审计日志才是可靠记录
    #（见 WARN 条目）。
    echo "⚠️  警告：检测到高风险操作：$pattern" >&2
  fi
done

if [ -n "$MATCHED_WARNINGS" ]; then
  log_decision "WARN:$MATCHED_WARNINGS"
  echo "   命令：$COMMAND" >&2
  echo "   继续——继续之前请审查上述警告。" >&2
else
  log_decision "ALLOW"
fi

# ── 允许 ─────────────────────────────────────────────────────────────────────
exit 0
