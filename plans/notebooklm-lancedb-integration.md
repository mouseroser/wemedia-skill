# NotebookLM + memory-lancedb-pro 集成方案

**制定日期**: 2026-03-09
**状态**: 探索阶段

---

## 一、集成目标

将 NotebookLM（云端知识库）与 memory-lancedb-pro（本地向量数据库）联合工作，实现：
- 记忆的分层存储和检索
- 知识的自动归档和沉淀
- 本地与云端的优势互补

---

## 二、当前架构分析

### memory-lancedb-pro
**优势**:
- ✅ 本地部署，响应快速
- ✅ 隐私安全，数据不出本地
- ✅ 支持 vector + BM25 混合检索
- ✅ 本地 rerank，精度高
- ✅ 与 OpenClaw 深度集成

**局限**:
- ❌ 只存储短文本片段（原子记忆）
- ❌ 缺少深度语义分析能力
- ❌ 不支持多模态内容
- ❌ 难以处理长文档

### NotebookLM
**优势**:
- ✅ Google AI 驱动，理解能力强
- ✅ 支持长文档和多模态
- ✅ 可生成报告、播客、思维导图等
- ✅ 自动提取关键信息和关联

**局限**:
- ❌ 云端服务，需要网络
- ❌ 数据隐私考虑
- ❌ API 调用有延迟
- ❌ 不适合高频实时查询

---

## 三、集成方案设计

### 方案 A: 分层检索架构

**原则**: 本地优先，云端补充

```
用户查询
  ↓
memory-lancedb-pro (本地快速检索)
  ↓ 如果命中率低或需要深度分析
NotebookLM (云端深度检索)
  ↓
融合结果返回
```

**实现**:
```python
def hybrid_recall(query, threshold=0.7):
    # 1. 先查本地
    local_results = memory_recall(query)
    
    # 2. 判断是否需要云端补充
    if local_results.confidence < threshold:
        # 查询 NotebookLM
        cloud_results = notebooklm_query(query)
        
        # 融合结果
        return merge_results(local_results, cloud_results)
    
    return local_results
```

**优势**:
- 快速响应（优先本地）
- 深度理解（必要时云端）
- 成本可控（按需调用）

### 方案 B: 自动归档流程

**原则**: 短期本地，长期云端

```
实时对话 → memory/*.md (markdown 日志)
  ↓ 实时写入
memory-lancedb-pro (向量数据库)
  ↓ 每周归档
NotebookLM (知识库)
```

**实现**:
```bash
# 每周日执行
# 1. 从 memory-lancedb-pro 导出高价值记忆
memory-pro export --scope agent:main --importance ">0.8" --output weekly-insights.md

# 2. 上传到 NotebookLM
notebooklm source add weekly-insights.md

# 3. 生成周报
notebooklm generate report

# 4. 下载并归档
notebooklm download report weekly-report-$(date +%Y-%m-%d).md
```

**优势**:
- 自动化归档
- 知识不丢失
- 便于长期回顾

### 方案 C: 双向增强

**原则**: 互相补充，各取所长

```
NotebookLM 生成的深度报告
  ↓ 提取关键结论
memory-lancedb-pro (作为原子记忆存储)
  ↓ 高频问题识别
NotebookLM (深度分析根因)
```

**实现**:
```bash
# 1. NotebookLM 生成报告后
notebooklm generate report
notebooklm download report analysis.md

# 2. 提取关键结论存入本地
cat analysis.md | extract_key_points.sh | while read line; do
    memory-pro store --text "$line" --category fact --importance 0.9
done

# 3. 定期分析本地高频问题
memory-pro stats --top-queries 10 > frequent-issues.txt

# 4. 上传到 NotebookLM 深度分析
notebooklm source add frequent-issues.txt
notebooklm ask "请分析这些高频问题的根本原因和系统性解决方案"
```

**优势**:
- 形成闭环
- 持续优化
- 知识沉淀

---

## 四、技术实现要点

### 4.1 数据格式转换

**memory-lancedb-pro → NotebookLM**:
```bash
# 导出为 markdown
memory-pro export --format markdown --output export.md

# 上传到 NotebookLM
notebooklm source add export.md
```

**NotebookLM → memory-lancedb-pro**:
```bash
# 下载报告
notebooklm download report report.md

# 提取关键点并存储
extract_key_points.sh report.md | while reane; do
    memory-pro store --text "$line" --category fact
done
```

### 4.2 查询路由策略

**何时查本地**:
- 高频问题（如"晨星是谁"）
- 最近对话上下文
- 配置和命令查询

**何时查云端**:
- 需要深度分析
- 跨领域关联查询
- 生成报告、总结等

**何时双查**:
- 重要决策
- 复杂问题排查
- 知识验证

### 4.3 隐私和安全

**敏感信息处理**:
```bash
# 上传前脱敏
sanitize_pii.sh input.md > sanitized.md
notebooklm source add sanitized.md
```

**分级存储**:
- 高敏感：只存本地（memory-lancedb-pro）
- 中敏感：脱敏后上传 NotebookLM
- 低敏感：直接上传 NotebookLM

---

## 五、实验验证计划

### 实验 1: 分层检索性能测试

**目标**: 验证本地+云端的检索效果

**步骤**:
1. 准备 100 个测试查询
2. 分别测试：
   - 只用 memory-lancedb-pro
   - 只用 NotebookLM
   - 分层检索（本地优先）
3. 对比：准确率、响应时间、成本

**成功标准**:
- 分层检索准确率 > 单独使用任一方
- 平均响应时间 < 2秒
- API 调用次数减少 50%+

### 实验 2: 自动归档效果验证

**目标**: 验证周期性归档的价值

**步骤**:
1. 运行 1 周，记录所有对话
2. 周末执行自动归档
3. 下周查询上周的问题
4. 对比归档前后的检索效果

**成功标准**:
- 上周问题的召回率 > 90%
- NotebookLM 能生成有价值的周报
- 本地数据库大小可控

### 实验 3: 双向增强闭环

**目标**: 验证知识循环的效果

**步骤**:
1. NotebookLM 生成深度分析报告
2. 提取关键结论存入本地
3. 1 周后统计这些结论的使用频率
4. 高频结论再次上传 NotebookLM 深化

**成功标准**:
- 提取的结论被实际使用
- 形成知识迭代循环
- 系统性问题得到解决

---

## 六、实施路线图

### Phase 1: 基础集成（1周）
- [ ] 实现 memory-lancedb-pro 导出脚本
- [ ] 实现 NotebookLM 批量上传脚本
- [ ] 验证数据格式兼容性

### Phase 2: 分层检索（2周）
- [ ] 实现查询路由逻辑
- [ ] 实现结果融合算法
- [ ] 性能测试和优化

### Phase 3: 自动归档（1周）
- [ ] 实现周期性归档脚本
- [ ] 配置 cron 任务
- [ ] 验证归档效果

### Phase 4: 双向增强（2周）
- [ ] 实现关键点提取
- [ ] 实现高频问题分析
- [ ] 建立知识循环机制

---

## 七、预期收益

### 短期收益（1个月）
- ✅ 记忆检索准确率提升 20%+
- ✅ 知识归档自动化
- ✅ 减少重复踩坑

### 中期收益（3个月）
- ✅ 形成完整的知识管理体系
- ✅ 本地+云端优势互补
- ✅ 系统性问题得到解决

### 长期收益（6个月+）
- ✅ 知识持续沉淀和迭代
- ✅ AI 辅助决策能力增强
- ✅ 团队知识共享

---

## 八、风险和应对

### 风险 1: 数据同步复杂度
**应对**: 先做单向同步，验证后再做双向

### 风险 2: 云端服务依赖
**应对**: 本地优先，云端作为补充

### 风险 3: 隐私泄露
**应对**: 严格的脱敏流程和分级存储

### 风险 4: 维护成本
**应对**: 高度自动化，减少人工干预

---

## 九、下一步行动

### 立即可做
1. 实验 memory-lancedb-pro 导出功能
2. 测试导出数据上传到 NotebookLM
3. 验证 NotebookLM 能否正确理解导出的记忆

### 本周目标
1. 完成 Phase 1 基础集成
2. 运行第一次自动归档
3. 收集初步反馈

### 本月目标
1. 完成 Phase 2 分层检索
2. 完成 Phase 3 自动归档
3. 开始 Phase 4 双向增强

---

**版本历史**:
- v1.0 (2026-03-09): 初版集成方案
