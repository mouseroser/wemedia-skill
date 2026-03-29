# Memory Noise Archive Fix — 2026-03-26

## 问题
尝试用 `memory_archive(query=...)` 归档系统包络噪音时失败。

## 根因
不是 `memory_archive` 本身坏了，而是：
- query 命中了多个候选
- 工具返回 `Multiple matches. Specify memoryId`
- 之前传的是短前缀或 query，不够唯一

## 修复
改为：
1. 先用 `memory_recall(..., includeFullText=true)` 找到目标条目
2. 拿到完整 memoryId
3. 再调用 `memory_archive(memoryId=<full-uuid>)`

## 已完成归档
- `ae9f450e-9779-4c41-a4a4-8b32ffb4dbc0`
- `4f130ed3-8b44-4272-be68-73b4bee9c11b`
- `42bade28-26d2-44b3-ba04-79eb167b1c84`

## 影响
这些 WhatsApp gateway / HEARTBEAT 系统包络噪音条目已从默认 recall 中移除，有助于降低 Layer 2 排序污染。

## 后续动作
- 继续按相同方法清理其余系统包络类噪音
- 对常见噪音模式建立一份可复用清单
