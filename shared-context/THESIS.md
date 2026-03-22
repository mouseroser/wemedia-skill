# THESIS.md - 当前世界观

## 我当前关注什么

### 核心理念
- **系统稳定优先**：任何新功能或优化都不能牺牲系统稳定性和可回滚性
- **可观察性第一**：通过文件系统、日志和监控群实现透明的多智能体协作
- **降本增效**：在保证质量的前提下，通过模型选择和架构优化降低成本
- **知道规则就执行**：不要问"要我...吗？"，这是晨星最强调的问题

### 关注领域
1. **OpenClaw 多智能体系统**
   - 星链流水线 v2.8（NotebookLM 证据驱动打磨层 + 动态模型分配）
   - 自媒体流水线 v1.1（Constitution-First 前置链）
   - 星鉴流水线 v1.2（轻量宪法 + NotebookLM 主研究）

2. **记忆系统优化**
   - memory-lancedb-pro + 本地 rerank sidecar + Layer 3 NotebookLM fallback
   - 三层记忆架构（MEMORY.md + 向量数据库 + NotebookLM）
   - 升级防护机制（post-upgrade-guard.sh）

3. **工具链完善**
   - NotebookLM 知识库（openclaw-docs, memory-archive, troubleshooting）
   - 本地 Ollama（bge-m3 embedding + bge-reranker-v2-m3 rerank）
   - Telegram 群组通知（12 个 agent 职能群 + 监控群）
   - Cron 分层管理（minimax 脚本型 / sonnet 工具型 / opus 编排型）

---

## 我已经写了什么

### 星链流水线 v2.8（2026-03-12）
- ✅ Main 直接编排所有 agent
- ✅ Review 改为单一审查任务
- ✅ NotebookLM 提前介入打磨层（Step 1.5B），证据驱动宪法
- ✅ Brainstorming 动态模型分配（L1/L2 sonnet, L3 opus）
- ✅ Spec-Kit 落地（brainstorming → analyze gate）
- ✅ 增强 Epoch 诊断与仲裁
- ✅ 预期降本 35-45%，效率提升 30-40%

### 自媒体流水线 v1.1（2026-03-06）
- ✅ Constitution-First 前置链
- ✅ NotebookLM 深度调研（M/L 级）
- ✅ 衍生内容生成（音频播客/思维导图/问答卡片）
- ✅ 晨星确认门控（未经确认绝不发布）

### 星鉴流水线 v1.2（2026-03-07）
- ✅ gemini 研究宪法
- ✅ claude 主方案
- ✅ review/gemini 一致性复核
- ✅ review/gpt 按需仲裁
- ✅ 首次完整运行验证通过（2026-03-13，Main 直接编排模式）

### 记忆系统三层架构（2026-03-07 - 2026-03-15）
- ✅ memory-lancedb-pro 部署 + 升级回归修复机制
- ✅ 本地 rerank sidecar（BAAI/bge-reranker-v2-m3，MPS加速）
- ✅ Layer 3 NotebookLM fallback 开发 + PR #206 提交
- ✅ 移除 openai SDK 依赖，改用原生 fetch 调本地 Ollama
- ✅ 升级守护脚本 post-upgrade-guard.sh（6小时自动修复）
- ✅ runtime worktree 与 PR worktree 分离
- ✅ P2.3 关闭：builtin memorySearch 不再作为双轨路线
- ✅ MEMORY.md 重构 + 定期维护 cron

### Agent 配置完善（2026-03-12）
- ✅ 为所有 12 个 agent 生成完整配置（SOUL.md, IDENTITY.md, HEARTBEAT.md）
- ✅ 每个 agent 都有独特的人格、emoji 和灵感来源
- ✅ 明确职责边界和硬性约束

### 运维优化（2026-03-15）
- ✅ Control UI hotfix 退役（OpenClaw 2026.3.13 已内置修复）
- ✅ Cron 第二轮稳态优化（minimax/sonnet/opus 分层）
- ✅ 路径索引 PATHS.md + Cron 总表 CRON-MATRIX.md
- ✅ openclaw-docs source 堆积问题修复（独立原子脚本）
- ✅ PR #210 合并（fork PR 跳过 claude-review）

### 3/16~22 周工作成果

#### 上游 PR 收口
- ✅ PR #206 被 maintainer 关闭（E2E 回归 + memory_recall 契约变更）
- ✅ PR #227 被关闭（测试未接入 npm test）
- ✅ 4H 上游路线明确暂缓执行，本地方案继续演进

#### Layer 3 稳定化 + 4F Spec-Kit
- ✅ Layer 3 fallback 改为直调 nlm-gateway.sh（绕过 gateway lane lock）
- ✅ L3 timeout 调高为 75 秒
- ✅ 5 个 NotebookLM cron 脚本全面修复并验证
- ✅ Layer 2 噪音过滤规则加固
- ✅ 4F.1-4F.5 全部完成（超时/重试/截断/JSON防御/触发阈值），4F.6-4F.7 数据驱动跳过
- ✅ 4E 观察期 8 天：L2 可用率 80%→87%，L3 从 0%→67%

#### Skills 精修
- ✅ notebooklm / starchain / wemedia / todo-manager skill 全部对齐当前架构

#### 自媒体运营系统 v1.1 落地
- ✅ 小红书方案 C+ 全链路验证（CDP 9223 + 独立 XiaohongshuProfiles）
- ✅ NLM media-research notebook 重建（id: 032a95b5）
- ✅ 累计 18 篇小红书内容发布，单日最高 12 条，爆款 Claude HUD 10K（690 观看/12.9% 互动率）
- ✅ NotebookLM infographic 生成能力验证（2048x2048 方图，全中文，CLI 全自动）
- ✅ 发现连发限流问题，建立 ≥30min 间隔规则
- ✅ Agent 安全系列封存（数据差，不适合小红书受众）

#### 硬性规则确认（3/20-21）
- ✅ 小红书发布禁用 MiniMax，必须用 Opus/Sonnet
- ✅ wemedia 创作禁用 MiniMax，必须用 Sonnet
- ✅ 操作类任务优先 GPT
- ✅ 发布前必须查记忆踩坑 / 检查重复 / 验证标题 ≤20 字 / 标签 ≤10 个

#### 基础设施
- ✅ MiniMax 切换到国内版 api.minimaxi.com
- ✅ web_search 修复（Brave Search 接管）
- ✅ 停用 profile=openclaw，改用 profile="user" 连本机 Chrome

---

## 还有哪些空白

### 短期空白（1-2 周）
- ⚠️ 星链流水线 v2.8 尚未完整执行验证
- ⚠️ 4H 上游路线暂缓执行（策略保留，等待合适时机重启）
- ⚠️ 自媒体从"量产"到"稳定高质量生产闭环"的衔接（已验证量产能力，需建立质量标准）
- ⚠️ gmncode.cn 代理残留清理（openclaw.json 第 69/138 行指向 52.7.156.79:19903）
- ⚠️ gemini agent 通用模式缺陷修复验证

### 中期空白（1-3 个月）
- ⚠️ enhanced_memory_recall 工具开发（L2→L3 自动降级）
- ⚠️ Ollama backend 作为 Smart Extraction LLM 的实验验证
- ⚠️ 星鉴流水线自动化报告生成
- ⚠️ 更多本地化 AI 工具链探索

### 长期空白
- ⚠️ 知识积累和经验传承的自动化
- ⚠️ 多智能体协作的可演进性
- ⚠️ 持续降本增效的机制

---

## 本周重大事件（2026-03-16 ~ 2026-03-22）

### 微信 ClawBot 发布（2026-03-22）
- 微信 8.0.70 推出官方 ClawBot 插件，支持 OpenClaw 接入微信
- 这是国民级超级 App 首次官方支持 OpenClaw
- 小红书首发"我的AI助手住进微信了"，先因配图问题删除后重发成功
- **教训**：NotebookLM infographic 生图必须用临时 notebook（单一干净 source），否则历史内容干扰

### 小红书账号受限（2026-03-22）
- 根因：单日连发 15 篇 + CDP 自动化被检测
- 违规原因：通过技术手段模拟用户操作
- **强制规则确立**：单日≤3篇、间隔≥3小时、申诉期间暂停；main 有最高制止权

### NotebookLM infographic 方案完善（2026-03-22）
- 确认 `--json` 输出 task_id → `download infographic` 下载本地
- 发现 notebook source 干扰问题，建立"临时 notebook + 单一干净 source"标准流程
- 临时 notebook 用完即删

### 硬规则确立
- nanobanana → nanobanana 改名完成（openclaw.json + 6个核心文件）
- wemedia 发布权下放（subagent 直接调用 publish_pipeline.py）
- skills 推送 GitHub（wemedia + media-tools）

---

## 下一步计划

### 明天（2026-03-23）
1. **等小红书账号解除限制**（约 01:23 到期）
2. **按新频率规则恢复发布**：单日≤3篇、间隔≥3小时
3. **Gem Antigravity 初稿**生图 + 发布（标题待确认）
4. **gmncode.cn 代理残留**清理（openclaw.json 第69/138行）

### 本周（2026-03-23 - 2026-03-29）
1. **自媒体生产闭环稳定化**：质量优先于数量，≥3小时间隔
2. **星链 v2.8 首次真实任务验证**
3. **基础设施清理**：gmncode.cn + gemini 通用模式

---

**最后更新**: 2026-03-22 23:50 (小光 周日维护)
**下次回顾**: 2026-03-29（每周日）
