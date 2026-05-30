# API 模块规范

本文件覆盖根 CLAUDE.md 中关于 /src/api/ 的所有内容

## API 专属规范

### 请求校验
- 使用 Zod 进行 schema 校验
- 始终校验输入
- 返回 400 及校验错误
- 包含字段级别的错误详情

### 身份验证
- 所有端点都需要 JWT token
- Token 放在 Authorization header 中
- Token 24 小时后过期
- 实现 refresh token 机制

### 响应格式

所有响应必须遵循以下结构：

```json
{
  "success": true,
  "data": { /* 实际数据 */ },
  "timestamp": "2025-11-06T10:30:00Z",
  "version": "1.0"
}
```

错误响应：
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "User message",
    "details": { /* 字段错误 */ }
  },
  "timestamp": "2025-11-06T10:30:00Z"
}
```

### 分页
- 使用基于游标的分页（不是 offset）
- 包含 `hasMore` 布尔值
- 最大页大小限制为 100
- 默认页大小：20

### 限流
- 已认证用户每小时 1000 次请求
- 公开端点每小时 100 次请求
- 超限时返回 429
- 包含 retry-after header

### 缓存
- 使用 Redis 进行会话缓存
- 默认缓存时长：5 分钟
- 写操作时失效
- 缓存 key 按资源类型打标签

---
**最后更新**：2026 年 4 月 9 日
