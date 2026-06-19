#!/bin/bash
# 校验用户 prompt
# Hook: UserPromptSubmit
#
# 从 stdin JSON 读取用户 prompt，阻断危险操作。
#
# 兼容：macOS、Linux、Windows（Git Bash）

# 从 stdin 读取 JSON 输入（Claude Code hook 协议）
INPUT=$(cat)

# 从 JSON 输入提取 prompt 文本
# Claude Code 的 UserPromptSubmit 字段为 "user_prompt"（回退到 "prompt"）
PROMPT=$(echo "$INPUT" | sed -n 's/.*"user_prompt"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
if [ -z "$PROMPT" ]; then
  PROMPT=$(echo "$INPUT" | sed -n 's/.*"prompt"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
fi

if [ -z "$PROMPT" ]; then
  exit 0
fi

# 检查危险操作
DANGEROUS_PATTERNS=(
  "rm -rf /"
  "delete database"
  "drop database"
  "format disk"
  "dd if="
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$PROMPT" | grep -qi "$pattern"; then
    printf '{"decision": "block", "reason": "检测到危险操作：%s"}' "$pattern"
    exit 0
  fi
done

# 检查生产部署
if echo "$PROMPT" | grep -qiE "(deploy|push).*production"; then
  if [ ! -f ".deployment-approved" ]; then
    echo '{"decision": "block", "reason": "生产部署需要审批。请创建 .deployment-approved 文件后再继续。"}'
    exit 0
  fi
fi

# 检查某些操作是否缺少必要上下文
if echo "$PROMPT" | grep -qi "refactor"; then
  if [ ! -d "tests" ] && [ ! -d "test" ]; then
    printf '{"additionalContext": "警告：没有测试就重构可能有风险。建议先写测试。"}'
  fi
fi

exit 0
