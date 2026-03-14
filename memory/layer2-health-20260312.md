# Layer 2 健康检查报告

**日期**: 2026-03-12 15:36:27

## 1. 向量数据库状态

- ❌ 数据库路径不存在: /Users/lucifinil_chen/.openclaw/data/memory-lancedb-pro

## 2. Rerank Sidecar 状态

- ✅ Rerank sidecar 运行正常

## 3. 自动捕获状态

- 今日自动捕获次数:        3
- ✅ 自动捕获正常工作

## 4. 召回质量检查

- ⚠️ memory-pro CLI 不可用，跳过召回测试

## 5. 健康评分

- ⚠️ **健康评分**: 50/100（一般）

## 6. 建议

- 检查 rerank sidecar 是否正常运行
- 运行 `bash ~/.openclaw/workspace/scripts/status-local-rerank-sidecar.sh`
- 如果需要重启：`launchctl kickstart -k gui/501/com.openclaw.local-rerank-sidecar`

---
**报告路径**: /Users/lucifinil_chen/.openclaw/workspace/memory/layer2-health-20260312.md
