# Memory Cron Tasks Optimization Plan

基于三层记忆架构优化 memory 相关的 cron 任务。

---

## 三层记忆架构回顾

### Layer 1: 本地文件（底层 - 原始记录）
- **文件**: memory/YYYY-MM-DD.md, MEMORY.md
- **用途**: 原始记录、可追溯、人类可读
- **维护**: 每周压缩检查（40k tokens 阈值）

### Layer 2: memory-lancedb-pro（中层 - 快速检索）
- **技术**: 向量检索 + BM25 + Rerank
- **用途**: 日常快速检索（90% 场景）
- **维护**: 自动捕获，按需补充原子记忆

### Layer 3: Memory Archive (NotebookLM)（顶层 - 深度理解）
- **Notebook ID**: bb3121a4-5e95-4d32-8d9a-a85cf1e3
- **用途**: 深度理解、长期归档、跨会话分析
- **维护**: 每月归档一次，生成月度摘要

---

## 当前 Cron 任务分析

### 现有任务

1. **memory-quality-audit**（每天 03:00）
   - 执行记忆质量审计
   - 生成审计报告
   - 有告警时推送通知
   - ✅ 保留，但需要增强

2. **daily-memory-report**（每天 05:00）
   - 生成每日记忆系统报告
   - 推送到晨星 DM + 监控群
   - ✅ 保留

3. **MEMORY.md 维护**（每周日 22:00）
   - 回顾本周日志
   - 提取重要内容到 MEMORY.md
   - 压缩超过 40k tokens 的日志
   - ✅ 保留，但需要增强

4. **troubleshooting-weekly-memory-update**（每周日 23:00）
   - 更新 troubleshooting notebook 中的 MEMORY.md
   - ⚠️ 需要调整为 Memory Archive

---

## 优化方案

### 新增任务

#### 1. Layer 2 健康检查（每天 02:00）
- **目的**: 检查 memory-lancedb-pro 的健康状态
- **任务**:
  - 检查向量数据库大小
  - 检查 rerank sidecar 状态
  - 检查自动捕获是否正常
  - 检查召回质量（漏召回监控）
- **频率**: 每天 02:00
- **模型**: minimax（降本）

#### 2. Layer 1 压缩检查（每周日 04:00）
- **目的**: 压缩超过阈值的每日日志
- **任务**:
  - 扫描 memory/YYYY-MM-DD.md 文件
  - 检查文件大小（40k tokens 阈值）
  - 压缩超过阈值的文件
  - 归档到 memory/archive/
- **频率**: 每周日 04:00
- **模型**: minimax（降本）

#### 3. Layer 3 月度归档（每月 1 号 01:00）
- **目的**: 将上月记忆归档到 Memory Archive (NotebookLM)
- **任务**:
  - 收集上月的 MEMORY.md 和重要日志
  - 上传到 Memory Archive notebook
  - 生成月度摘要
  - 清理本地旧文件
- **频率**: 每月 1 号 01:00
- **模型**: opus（高质量）

#### 4. Layer 3 深度洞察（每月 15 号 01:00）
- **目的**: 使用 NotebookLM 生成深度洞察
- **任务**:
  - 查询 Memory Archive
  - 生成跨会话分析
  - 识别模式和趋势
  - 生成改进建议
- **频率**: 每月 15 号 01:00
- **模型**: opus（高质量）

### 调整现有任务

#### 1. memory-quality-audit（增强）
- **新增检查项**:
  - Layer 1: 文件完整性
  - Layer 2: 向量数据库健康
  - Layer 3: NotebookLM 同步状态
- **生成三层架构健康报告**

#### 2. MEMORY.md 维护（增强）
- **新增步骤**:
  - 检查是否需要归档到 Layer 3
  - 更新 MEMORY-ARCHITECTURE.md
  - 同步到 Memory Archive（如果有重大更新）

#### 3. troubleshooting-weekly-memory-update（调整）
- **改名**: memory-archive-weekly-sync
- **新任务**:
  - 同步 MEMORY.md 到 Memory Archive
  - 同步本周重要日志到 Memory Archive
  - 生成周度摘要

---

## 完整 Cron 任务时间表

| 时间 | 任务 | 频率 | Layer | 模型 |
|------|------|------|-------|------|
| 02:00 | Layer 2 健康检查 | 每天 | Layer 2 | minimax |
| 03:00 | memory-quality-audit（增强） | 每天 | All | minimax |
| 04:00 | Layer 1 压缩检查 | 每周日 | Layer 1 | minimax |
| 05:00 | daily-memory-report | 每天 | All | opus |
| 22:00 | MEMORY.md 维护（增强） | 每周日 | Layer 1 | opus |
| 23:00 | memory-archive-weekly-sync | 每周日 | Layer 3 | opus |
| 01:00 | Layer 3 月度归档 | 每月 1 号 | Layer 3 | opus |
| 01:00 | Layer 3 深度洞察 | 每月 15 号 | Layer 3 | opus |

---

## 实施步骤

### Phase 1: 立即实施（本周）
1. ✅ 创建 Layer 2 健康检查脚本
2. ✅ 创建 Layer 1 压缩检查脚本
3. ✅ 增强 memory-quality-audit
4. ✅ 调整 troubleshooting-weekly-memory-update

### Phase 2: 下周实施
1. ⚠️ 创建 Layer 3 月度归档脚本
2. ⚠️ 创建 Layer 3 深度洞察脚本
3. ⚠️ 测试所有新任务

### Phase 3: 观察期（1 个月）
1. ⚠️ 监控任务执行情况
2. ⚠️ 收集反馈
3. ⚠️ 调整频率和参数

---

## 预期收益

### 短期（1-2 周）
- ✅ Layer 2 健康状态可观察
- ✅ Layer 1 文件大小可控
- ✅ 三层架构健康报告

### 中期（1-3 个月）
- ✅ Memory Archive 充分利用
- ✅ 月度摘要和洞察
- ✅ 跨会话分析能力

### 长期
- ✅ 知识积累和经验传承自动化
- ✅ 模式识别和趋势分析
- ✅ 持续改进建议

---

**创建时间**: 2026-03-12 15:35
**维护者**: main (小光)
