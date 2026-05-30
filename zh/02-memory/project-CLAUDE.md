# 项目配置

## 项目概览
- **项目名称**：E-commerce Platform
- **技术栈**：Node.js, PostgreSQL, React 18, Docker
- **团队规模**：5 名开发者
- **截止日期**：2025 年 Q4

## 架构
@docs/architecture.md
@docs/api-standards.md
@docs/database-schema.md

## 开发规范

### 代码风格
- 使用 Prettier 格式化
- 使用 ESLint + airbnb 配置
- 最大行宽：100 字符
- 使用 2 空格缩进

### 命名约定
- **文件**：kebab-case（user-controller.js）
- **类**：PascalCase（UserService）
- **函数/变量**：camelCase（getUserById）
- **常量**：UPPER_SNAKE_CASE（API_BASE_URL）
- **数据库表**：snake_case（user_accounts）

### Git 工作流
- 分支命名：`feature/description` 或 `fix/description`
- Commit 信息：遵循 conventional commits
- 合并前必须有 PR
- 所有 CI/CD 检查必须通过
- 至少需要 1 个审批

### 测试要求
- 最低 80% 代码覆盖率
- 所有关键路径必须有测试
- 单元测试使用 Jest
- E2E 测试使用 Cypress
- 测试文件命名：`*.test.ts` 或 `*.spec.ts`

### API 规范
- 仅使用 RESTful 端点
- JSON 请求/响应
- 正确使用 HTTP 状态码
- API 端点版本化：`/api/v1/`
- 所有端点需附带示例文档

### 数据库
- 使用 migration 进行 schema 变更
- 永远不要硬编码凭证
- 使用连接池
- 开发环境启用查询日志
- 定期备份

### 部署
- 基于 Docker 的部署
- Kubernetes 编排
- 蓝绿部署策略
- 失败时自动回滚
- 部署前先运行数据库 migration

## 常用命令

| 命令 | 用途 |
|------|------|
| `npm run dev` | 启动开发服务器 |
| `npm test` | 运行测试套件 |
| `npm run lint` | 检查代码风格 |
| `npm run build` | 构建生产版本 |
| `npm run migrate` | 运行数据库迁移 |

## 团队联系人
- Tech Lead：Sarah Chen (@sarah.chen)
- Product Manager：Mike Johnson (@mike.j)
- DevOps：Alex Kim (@alex.k)

## 已知问题与解决办法
- PostgreSQL 连接池在高峰期限制为 20
- 解决办法：实现查询排队
- Safari 14 与 async generators 存在兼容性问题
- 解决办法：使用 Babel 转译

## 相关项目
- Analytics Dashboard：`/projects/analytics`
- Mobile App：`/projects/mobile`
- Admin Panel：`/projects/admin`

---
**最后更新**：2026 年 4 月 9 日
