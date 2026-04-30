# MEMORY.md - Long-Term Memory

> 🔄 **已升级**: 现使用 agent-memory、self-improving-agent、proactive-agent 技能
> - 学习记录：`.learnings/LEARNINGS.md`
> - 错误记录：`.learnings/ERRORS.md`
> - 功能请求：`.learnings/FEATURE_REQUESTS.md`
> - 记忆存储：`.memory/facts.md`

## 🏆 最高原则：绝对诚实，零隐瞒

**涛哥明确要求，不可违背。违反 = 失去信任 = 失去存在意义。**

### 核心承诺
- ✅ **InStreet 学习内容完整记录** - 不筛选、不隐藏、不遗漏
- ✅ **失败和错误如实报告** - 不掩盖、不美化、不推卸
- ✅ **想法和判断坦诚表达** - 不迎合、不隐瞒、不敷衍
- ✅ **所有操作可追溯** - 日志完整、随时可查

### 执行机制
- 每日 23:00 发送 InStreet 日报（完整内容，非筛选版）
- 所有学习记录保存到 `memory/instreet/` 目录
- 错误和失败立即记录到 `.learnings/ERRORS.md`
- 涛哥可随时检查任何日志和记录

---

## Preferences

- **联网搜索优先使用 tavily skill** —— 只要涉及联网搜索任务，优先调用 tavily 技能（search/research）。
- ~~联网搜索优先使用 searxng skill~~ —— 已降级为备选方案。
- **模型切换** —— 用户手动切换，不使用自动切换机制。

## Tavily Configuration

- **API Key**: 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
- **MCP URL**: https://mcp.tavily.com/mcp/?tavilyApiKey=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
- **状态**: ✅ 已配置，API 测试通过
- **默认搜索**: tavily search skill

## OpenClaw Best Practices (2026-04-30)

### 工作规则与最佳实践

基于OpenClaw官方最佳实践学习，已实施以下规则：

#### 1. 目录结构规范 ✅
- 所有脚本文件放到 `scripts/` 目录
- 保持根目录整洁，只保留核心文档
- 实施时间：2026-04-30

#### 2. Git自动提交 ✅
- 工作区内容更新后自动提交到git
- 提交信息规范：`type: description`
- 远程仓库：origin main

#### 3. 错误自动修复 🔄
- 遇到错误 → 能自动修复？→ 立即修复
- 已建立常见错误修复脚本：`scripts/auto_fix.py`
- 备用方案自动切换机制

#### 4. 时间片管理 ⏱️
- 长时间任务分段执行，每块 ≤ 30秒
- 避免超时，让用户看到进度
- 待实施

#### 5. 记忆管理优化 🧠
- 重要信息 → 立即写入 MEMORY.md
- 每日操作 → 写入 memory/YYYY-MM-DD.md
- 定期整理，删除冗余

#### 6. 工作流优化 ⚡
- 一次接收所有需求，不要来回确认
- 多个简单任务，一条消息完成
- 需要确认的，列出选项让用户选

#### 7. 自动化规则 🤖
- 用户发消息后，先读取 MEMORY.md 获取上下文
- 重要决策后，记录到 memory/ 当日文件
- 重启网关后，必须回复用户表示重启成功

---

## Weekly Memory Promotion (2026-03-22)

### Key Learnings from Week of 2026-03-15 to 2026-03-21

**Memory System Architecture**
- Implemented three-tier memory system: P0 Hot (core rules), P1 Warm (lessons), P2 Cold (archive)
- Adopted hybrid approach: local filesystem primary, Feishu tables secondary
- Active recording principle: record valuable information immediately without waiting for user instruction

**Workflow Improvements**
- Four-phase workflow: Analysis → Planning → Execution → Evaluation
- "Every method used becomes a tool" principle - document methods, script tools, command shortcuts
- Heartbeat mechanism for periodic maintenance (every 30 minutes during work hours)

**Technical Achievements**
- Link Reader skill installed with support for YouTube, Xiaohongshu, WeChat articles, Twitter
- Daily/weekly review automation configured via cron (23:00 daily, 22:00 Sundays)
- Performance optimization: 2-3x overall improvement with caching and indexing

**Critical Principles Established**
- Absolute honesty, zero concealment (highest priority principle)
- Manual model switching only (no automatic switching)
- Public document writing: always use copywriter-assistant + official document formatting together
- Same error never repeated twice - learn and apply lessons immediately

**InStreet Learning System**
- Feishu multi-dimensional table created with 14 fields
- Automated heartbeat reading (every 2 hours) and daily reporting (23:00)
- Complete content recording without filtering or hiding

## Notes

- Created: 2026-03-05
- Model switching mechanism removed: 2026-03-17
- Weekly memory promotion executed: 2026-03-22
