#!/bin/bash
# 记录所有 bash 命令
# Hook: PostToolUse:Bash
#
# 从 stdin JSON 读取已执行的命令并记录到文件。
#
# 兼容：macOS、Linux、Windows（Git Bash）

# 从 stdin 读取 JSON 输入（Claude Code hook 协议）
INPUT=$(cat)

# 从 tool_input 提取 bash 命令
# 注意：sed 的 [^"]* 会在 JSON 转义引号处停止；对于含双引号字符串的命令，
# 只会捕获到第一个 \" 之前的部分——这是基于 sed 解析 JSON 的已知局限，
# 用于日志记录场景可以接受。
COMMAND=$(echo "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$COMMAND" ]; then
  exit 0
fi

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
LOGFILE="$HOME/.claude/bash-commands.log"

# 若日志目录不存在则创建
mkdir -p "$(dirname "$LOGFILE")"

# 记录命令
echo "[$TIMESTAMP] $COMMAND" >> "$LOGFILE"

exit 0
