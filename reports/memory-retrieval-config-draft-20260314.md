# Memory Retrieval Config Draft — 2026-03-14

## 结论先行
**今天不建议直接应用配置。**

原因不是策略本身有问题，而是：
- builtin memorySearch 当前被 `memory/archive/` 中超长文件拖垮
- 在这个问题解决前，启用 hybrid / MMR / temporalDecay / sessionMemory 也很难得到干净评估结果

---

## 一、理论上值得尝试的最小风险配置

### 目标
在不替换主插件的前提下，增强 builtin memorySearch 的排序质量：
- hybrid：兼顾语义和关键词
- MMR：降低重复
- temporalDecay：降低旧记忆抢排位
- sessionMemory：补齐短期会话召回

### 草案 patch（暂不应用）
```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "experimental": {
          "sessionMemory": true
        },
        "query": {
          "maxResults": 8,
          "minScore": 0.15,
          "hybrid": {
            "enabled": true,
            "vectorWeight": 0.7,
            "textWeight": 0.3,
            "candidateMultiplier": 4,
            "mmr": {
              "enabled": true,
              "lambda": 0.7
            },
            "temporalDecay": {
              "enabled": true,
              "halfLifeDays": 30
            }
          }
        }
      }
    }
  }
}
```

---

## 二、当前真正的阻塞点

### 阻塞点 1：archive 布局与 builtin 默认索引范围冲突
builtin memorySearch 默认索引：
- `MEMORY.md`
- `memory/**/*.md`

而当前超大归档文件仍在：
- `memory/archive/notebooklm-daily-20260313.md`
- `memory/archive/notebooklm-daily-20260314.md`

导致实际 search 时出现：
```text
Ollama embeddings HTTP 500: the input length exceeds the context length
```

### 阻塞点 2：sessionMemory 尚未完整启用
虽然配置里写了：
```json
"sources": ["memory", "sessions"]
```
但当前 status 实际只看到 `memory`。

这意味着 session transcript recall 并未真正进入可评估状态。

---

## 三、因此推荐的执行顺序

### Stage 0（先做）
1. 完成 benchmark
2. 确认 archive 是否需要移出 `memory/`
3. 决定 builtin memorySearch 是：
   - shadow lane
   - 还是正式辅助链路

### Stage 1（确认后再做）
如果决定继续评估 builtin memorySearch，则：
1. 先处理 archive 索引冲突
2. 再应用 hybrid / MMR / temporalDecay / sessionMemory
3. 观察 7 天后再决定是否长期保留

---

## 四、子 Agent builtin memorySearch 治理建议

当前多个 agent 的 builtin memorySearch 状态为：
- dirty
- memory directory missing
- indexed 0

### 建议方案
**推荐：保持 main 为主要评估对象，不急着给所有 agent 补 memory 目录。**

原因：
- 现在要优化的是 main 的记忆质量，不是所有 agent 的 builtin index 完整性
- 给每个 agent 补目录只会增加噪音维护成本
- 真正需要用时，再按 agent 单独治理更合理

---

## 五、一句话结论
> 现在不是“该不该开 hybrid/MMR/temporalDecay”的问题，而是“builtin memorySearch 在当前 archive 布局下还没到可公平评估的状态”。

所以：
- 配置草案已准备好
- **但暂不应用**
- 先解决 benchmark 和 archive 冲突，再决定下一步