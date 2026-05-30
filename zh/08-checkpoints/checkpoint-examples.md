# Checkpoint 示例

在 Claude Code 中高效使用 checkpoints 的真实场景示例。

注意：Checkpoints 会在每次用户提示时自动创建。你无需手动保存。要回退，请按两次 `Esc`（`Esc+Esc`）或使用 `/rewind` 打开 checkpoint 浏览器。

## 示例 1：数据库迁移

### 场景
你需要从 MySQL 迁移到 PostgreSQL，但想同时探索直接迁移和渐进式双写两种方案。

### 工作流

```
User: 我们来实现从 MySQL 到 PostgreSQL 的直接迁移
      [Checkpoint A 自动创建]

Claude: 我来实现直接迁移……
[更换数据库驱动、更新查询、修改 schema]

User: 运行测试
      [Checkpoint B 自动创建]

Claude: 正在运行测试……
❌ 15 个测试失败 — 连接池问题

User: 这个方案有问题。我们改用双写模式。
[用户按下 Esc+Esc，选择 Checkpoint A，选择「恢复代码和对话」]

User: 现在实现双写模式，同时向两个数据库写入

Claude: 我来实现双写迁移……
[实现双写层、渐进式迁移策略]

User: 运行测试

Claude: 正在运行测试……
✅ 全部测试通过

User: 双写方案明显更稳妥。提交这个版本。
```

## 示例 2：性能优化

### 场景
尝试多种性能优化策略。

### 工作流

```
User: 优化一下 API 响应时间。当前：450ms
      [Checkpoint "Baseline" 自动创建]

Claude: 我来添加数据库查询缓存……
[实现 Redis 缓存]

User: 运行性能测试

Claude: 结果：平均响应时间 280ms（提升 38%）

User: 换个方案试试。
[用户按下 Esc+Esc，选择 "Baseline" checkpoint，选择「恢复代码和对话」]

User: 试试数据库查询优化

Claude: 我来优化数据库查询……
[添加索引，优化 N+1 查询]

User: 运行性能测试

Claude: 结果：平均响应时间 180ms（提升 60%）

User: 再试第三个方案。
[用户按下 Esc+Esc，选择 "Baseline" checkpoint，选择「恢复代码和对话」]

User: 试试响应压缩和 CDN

Claude: 我来添加压缩和 CDN……
[实现 gzip，配置 CDN]

User: 运行性能测试

Claude: 结果：平均响应时间 320ms（提升 29%）

User: 查询优化效果最好。让我回到那个版本，然后和缓存结合起来。
[用户按下 Esc+Esc，选择查询优化后的 checkpoint，选择「恢复代码和对话」]

User: 现在在优化后的查询之上添加 Redis 缓存

Claude: [在优化后的查询之上添加 Redis 缓存]

User: 运行性能测试

Claude: 结果：平均响应时间 95ms（提升 79%）🎉

User: 完美！这就是最佳方案。提交它。
```

## 示例 3：UI/UX 迭代

### 场景
为仪表板尝试不同布局。

### 工作流

```
User: 把仪表板重设计成侧边栏布局
      [Checkpoint "Start" 自动创建]

Claude: [实现侧边栏布局]

User: 给我看截图

Claude: [显示截图]

User: 侧边栏太拥挤了。试试顶部导航。
[用户按下 Esc+Esc，选择 "Start" checkpoint，选择「恢复代码和对话」]

User: 试试顶部导航布局

Claude: [实现顶部导航]

User: 给我看截图

Claude: [显示截图]

User: 好多了，不过再试试卡片式网格布局。
[用户按下 Esc+Esc，选择 "Start" checkpoint，选择「恢复代码和对话」]

User: 试试卡片式网格布局

Claude: [实现卡片网格]

User: 给我看截图

Claude: [显示截图]

User: 这个很棒！不过能把顶部导航和卡片网格结合起来吗？
[用户按下 Esc+Esc，选择卡片网格后的 checkpoint，选择「恢复代码和对话」]

User: 给卡片网格布局加上顶部导航

Claude: [在卡片网格上添加顶部导航]

User: 完美！这就是最终设计。
```

## 示例 4：调试会话

### 场景
用多种假设排查一个棘手的 bug。

### 工作流

```
User: 应用有内存泄漏
      [Checkpoint "Before debugging" 自动创建]

Claude: 我来排查……
[分析代码]

User: 我觉得问题出在事件监听器上。先修这里。

Claude: [修复事件监听器清理逻辑]

User: 运行内存分析器

Claude: 仍然在泄漏 — 事件监听器不是问题所在

User: 回退，换个假设试试。
[用户按下 Esc+Esc，选择 "Before debugging" checkpoint，选择「恢复代码和对话」]

User: 会不会是数据库连接？

Claude: [实现连接池修复]

User: 运行内存分析器

Claude: 还在泄漏 — 也不是连接的问题

User: 再回退，换个方向查。
[用户按下 Esc+Esc，选择 "Before debugging" checkpoint，选择「恢复代码和对话」]

User: 查一下有没有循环引用

Claude: [找到并修复缓存中的循环引用]

User: 运行内存分析器

Claude: ✅ 内存泄漏已修复！缓存层的循环引用就是罪魁祸首。

User: 太好了！提交这个修复。
```

## 示例 5：API 设计演进

### 场景
对 REST API 设计进行多轮迭代。

### 工作流

```
User: 为我们的博客平台创建一个 REST API
      [Checkpoint "Before API design" 自动创建]

Claude: [创建基础 CRUD API]

User: 这太简单了。加上分页和过滤

Claude: [添加分页和过滤]

User: 需要更好的资源关系

Claude: [实现 HATEOAS 链接]

User: 其实，我们试试用 GraphQL 替代 REST
[用户按下 Esc+Esc，选择 "Before API design" checkpoint，选择「恢复代码和对话」]

User: 为博客平台实现 GraphQL API

Claude: [实现 GraphQL API]

User: 还是觉得 REST 更适合我们的场景。
[用户按下 Esc+Esc，选择 HATEOAS 之后的 checkpoint，选择「恢复代码和对话」]

User: 把 REST 方案最终定下来。
```

## 示例 6：配置管理

### 场景
测试不同的配置方案。

### 工作流

```
User: 把配置迁移到环境变量
      [Checkpoint "Original config" 自动创建]

Claude: [实现环境变量配置]

User: 在开发环境测试

Claude: 本地可用，但生产环境部署有问题

User: 换个方案试试。
[用户按下 Esc+Esc，选择 "Original config" checkpoint，选择「恢复代码和对话」]

User: 试试带校验的配置文件方案

Claude: [实现带 JSON Schema 校验的 YAML 配置]

User: 在开发环境测试

Claude: ✅ 运行良好，校验错误提示清晰

User: 能不能也为敏感值支持环境变量？

Claude: [为密钥添加环境变量覆盖]

User: 测试部署

Claude: ✅ 所有环境均正常运行

User: 完美！这个可以上生产环境了。
```

## 示例 7：测试策略

### 场景
实现全面的测试体系。

### 工作流

```
User: 为 auth 模块添加单元测试
      [Checkpoint 自动创建]

Claude: [添加 Jest 单元测试]

User: 运行测试

Claude: 45 个测试通过，覆盖率 78%

User: 再加集成测试

Claude: [添加集成测试]

User: 运行测试

Claude: 89 个测试通过，覆盖率 92%，但测试太慢（3 分钟）

User: 测试太慢了。优化一下。

Claude: [优化测试准备，添加并行执行]

User: 运行测试

Claude: 89 个测试通过，覆盖率 92%，耗时 35 秒 ✅

User: 很好！再给关键路径加 E2E 测试。

Claude: [添加 Playwright E2E 测试]

User: 运行全部测试

Claude: 112 个测试通过，覆盖率 94%，耗时 2 分钟

User: 覆盖率和速度平衡得刚刚好！
```

## 示例 8：从 Checkpoint 开始总结

### 场景
长时间调试会话后，你想压缩对话内容，同时保留上下文。

### 工作流

```
User: [经过 20 多条调试和探索消息之后]

[用户按下 Esc+Esc，选择较早的 checkpoint，选择「从这里开始总结」]
[可选地提供指令："重点记录我们尝试了什么、哪些有效"]

Claude: [生成从该点往后的对话总结]
[原始消息保留在记录中]
[总结替代可见对话，减少上下文窗口占用]

User: 现在继续推进那个有效的方案。
```

## 关键要点

1. **Checkpoints 是自动的**：每次用户提示都会创建 checkpoint — 无需手动保存
2. **使用 Esc+Esc 或 /rewind**：这是打开 checkpoint 浏览器的两种方式
3. **选择合适的恢复选项**：根据需要恢复代码、对话、两者都恢复或总结
4. **不要害怕试验**：Checkpoints 让你可以安全地尝试大幅改动
5. **与 git 结合使用**：用 checkpoints 进行探索，用 git 保存最终落地的成果
6. **长会话要总结**：使用「从这里开始总结」保持对话可管理

---
**最后更新**：2026 年 5 月 20 日
**Claude Code 版本**：2.1.145
**来源**：
- https://code.claude.com/docs/en/checkpointing
- https://code.claude.com/docs/en/changelog
**兼容模型**：Claude Sonnet 4.6、Claude Opus 4.7、Claude Haiku 4.5
