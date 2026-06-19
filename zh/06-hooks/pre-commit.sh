#!/bin/bash
# 提交前运行测试
# Hook: PreToolUse（matcher: Bash）—— 检查命令是否为 git commit
# 注意：没有 "PreCommit" hook 事件。用 PreToolUse 配合 Bash matcher，
# 检查命令以检测 git commit 操作。

echo "🧪 提交前正在运行测试..."

# 检查是否存在 package.json（Node.js 项目）
if [ -f "package.json" ]; then
  if grep -q "\"test\":" package.json; then
    npm test
    if [ $? -ne 0 ]; then
      echo "❌ 测试失败！提交已阻断。"
      exit 1
    fi
  fi
fi

# 检查 pytest 是否可用（Python 项目）
if [ -f "pytest.ini" ] || [ -f "setup.py" ]; then
  if command -v pytest &> /dev/null; then
    pytest
    if [ $? -ne 0 ]; then
      echo "❌ 测试失败！提交已阻断。"
      exit 1
    fi
  fi
fi

# 检查是否存在 go.mod（Go 项目）
if [ -f "go.mod" ]; then
  go test ./...
  if [ $? -ne 0 ]; then
    echo "❌ 测试失败！提交已阻断。"
    exit 1
  fi
fi

# 检查是否存在 Cargo.toml（Rust 项目）
if [ -f "Cargo.toml" ]; then
  cargo test
  if [ $? -ne 0 ]; then
    echo "❌ 测试失败！提交已阻断。"
    exit 1
  fi
fi

echo "✅ 所有测试通过！继续提交。"
exit 0
