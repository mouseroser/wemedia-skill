# Spawn 任务标准格式

## 统一任务包装结构

所有 agent spawn 任务应使用以下标准格式：

```
[PIPELINE]: 星链 | 星鉴 | 自媒体
[STEP]: Step 1.5A | Step 1.5B | Step 4 | Step 5 ...
[ROLE]: scan | constitution | planning | review | arbitration | coding | test
[LEVEL]: L1/L2/L3 或 Q/S/D
[GOAL]: 本次任务的核心目标
[CONTEXT]: 任务上下文和背景
[INPUT_FILES]: 输入文件路径列表
[OUTPUT_PATH]: 输出文件路径
[REQUIRED_OUTPUT]: 必须输出的内容结构
[NOTIFY_TARGETS]: 通知目标（群ID列表）
[STOP_CONDITIONS]: 停止条件
```

## 示例 1: Step 1.5A Gemini 扫描

```javascript
sessions_spawn({
  agentId: "gemini",
  mode: "run",
  model: "gemini/gemini-3.1-pro-preview",
  thinking: "medium",
  task: `
[PIPELINE]: 星链
[STEP]: Step 1.5A
[ROLE]: scan
[LEVEL]: L2
[GOAL]: 需求歧义扫描，识别边界、假设、风险
[CONTEXT]: ${原始需求描述}
[INPUT_FILES]: 
  - 原始需求文档
  - 用户描述
[OUTPUT_PATH]: ~/.openclaw/workspace/agents/gemini/reports/scan-${timestamp}.md
[REQUIRED_OUTPUT]:
  1. 任务目标
  2. 关键歧义
  3. 边界条件
  4. 默认假设
  5. 风险清单
  6. 需要被宪法固定的硬约束
  7. 红线列表
[NOTIFY_TARGETS]:
  - 织梦群 (-5264626153)
  - 监控群 (-5131273722)
[STOP_CONDITIONS]:
  - 不写实现代码
  - 不直接出最终方案
  `,
  runTimeoutSeconds: 300
})
```

## 示例 2: Step 1.5B OpenAI 宪法

```javascript
sessions_spawn({
  agentId: "openai",
  mode: "run",
  model: "openai/gpt-5.4",
  thinking: "medium",
  task: `
[PIPELINE]: 星链
[STEP]: Step 1.5B
[ROLE]: constitution
[LEVEL]: L2
[GOAL]: 基于 Gemini 扫描结果产出最终宪法
[CONTEXT]: ${Gemini扫描结果摘要}
[INPUT_FILES]:
  - ${gemini_scan_file}
  - 原始任务描述
[OUTPUT_PATH]: ~/.openclaw/workspace/agents/openai/reports/constitution-${timestamp}.md
[REQUIRED_OUTPUT]:
  1. 目标（P0/P1/P2）
  2. 非目标
  3. 硬约束
  4. 验收标准
  5. 风险
  6. 默认假设
  7. 红线
  8. 最终输出契约
[NOTIFY_TARGETS]:
  - openai 群 (-5242027093)
  - 监控群 (-5131273722)
[STOP_CONDITIONS]:
  - 只做规则收敛，不做实现设计
  - 不替代 Claude 的方案设计职责
  `,
  runTimeoutSeconds: 300
})
```

## 示例 3: Step 1.5C Claude 实施计划

```javascript
sessions_spawn({
  agentId: "claude",
  mode: "run",
  model: "anthropic/claude-opus-4-6",
  thinking: "medium",
  task: `
[PIPELINE]: 星链
[STEP]: Step 1.5C
[ROLE]: planning
[LEVEL]: L2
[GOAL]: 基于最终宪法产出可执行的实施计划
[CONTEXT]: ${宪法摘要}
[INPUT_FILES]:
  - ${constitution_file}
  - 原始任务上下文
[OUTPUT_PATH]: ~/.openclaw/workspace/agents/claude/reports/plan-${timestamp}.md
[REQUIRED_OUTPUT]:
  1. 宪法复述
  2. 实施目标
  3. 方案说明
  4. 影响面
  5. 文件/模块级改动点
  6. 测试策略
  7. 回滚方案
  8. 风险与依赖
  9. 执行顺序
[NOTIFY_TARGETS]:
  - 小克群 (-5101947063)
  - 监控群 (-5131273722)
[STOP_CONDITIONS]:
  - 优先最小改动和最低风险
  - 不写空泛原则，只写可执行步骤
  - 不擅自改写宪法
  `,
  runTimeoutSeconds: 300
})
```

## 示例 4: Step 1.5D Review(Gemini) 一致性复核

```javascript
sessions_spawn({
  agentId: "review",
  mode: "run",
  model: "anthropic/claude-sonnet-4-6",
  thinking: "medium",
  task: `
[PIPELINE]: 星链
[STEP]: Step 1.5D
[ROLE]: review
[LEVEL]: L2
[GOAL]: 编排 gemini 检查 Claude 计划是否偏离宪法
[CONTEXT]: ${宪法摘要} + ${Claude计划摘要}
[INPUT_FILES]:
  - ${constitution_file}
  - ${claude_plan_file}
[OUTPUT_PATH]: ~/.openclaw/workspace/agents/review/reports/review-1.5D-${timestamp}.md
[REQUIRED_OUTPUT]:
  1. 结论：ALIGN / DRIFT / MAJOR_DRIFT
  2. 违反宪法的点
  3. 漏掉的边界
  4. 错误假设
  5. 风险遗漏
  6. 必改项
  7. 可忽略项
[NOTIFY_TARGETS]:
  - 交叉审核群 (-5242448266)
  - 监控群 (-5131273722)
[STOP_CONDITIONS]:
  - 不重写整套计划
  - 每条问题都要对应宪法依据
[SUB_AGENT]: gemini
[SUB_AGENT_THINKING]: medium
  `,
  runTimeoutSeconds: 300
})
```

## 示例 5: Step 1.5E Review(OpenAI) 仲裁

```javascript
sessions_spawn({
  agentId: "review",
  mode: "run",
  model: "anthropic/claude-sonnet-4-6",
  thinking: "high",
  task: `
[PIPELINE]: 星链
[STEP]: Step 1.5E
[ROLE]: arbitration
[LEVEL]: L3
[GOAL]: 编排 openai 仲裁 Claude 计划与 Gemini 复核分歧
[CONTEXT]: ${宪法摘要} + ${Claude计划摘要} + ${Gemini复核结果}
[INPUT_FILES]:
  - ${constitution_file}
  - ${claude_plan_file}
  - ${gemini_review_file}
[OUTPUT_PATH]: ~/.openclaw/workspace/agents/review/reports/arbitration-1.5E-${timestamp}.md
[REQUIRED_OUTPUT]:
  1. 结论：GO / REVISE / BLOCK
  2. 逐条裁决
  3. 必须修改项
  4. 可忽略项
  5. 最终执行指令
[NOTIFY_TARGETS]:
  - 交叉审核群 (-5242448266)
  - 监控群 (-5131273722)
[STOP_CONDITIONS]:
  - 宪法是唯一最高依据
  - 不要重写整套方案
  - 输出唯一结论，不要模糊措辞
[SUB_AGENT]: openai
[SUB_AGENT_THINKING]: high
  `,
  runTimeoutSeconds: 300
})
```

## 示例 6: Step 4 Coding 修复

```javascript
sessions_spawn({
  agentId: "coding",
  mode: "run",
  model: "openai/gpt-5.4", // Type B
  thinking: "medium",
  task: `
[PIPELINE]: 星链
[STEP]: Step 4
[ROLE]: coding
[LEVEL]: L2
[GOAL]: 执行修复，严格依据计划和 review 结论
[CONTEXT]: ${修复清单}
[INPUT_FILES]:
  - ${constitution_file}
  - ${approved_plan_file}
  - ${review_verdict_file}
  - ${patch_scope}
[OUTPUT_PATH]: ~/.openclaw/workspace/agents/coding/
[REQUIRED_OUTPUT]:
  1. 修复范围
  2. 修复动作
  3. 涉及文件
  4. 冒烟结果
  5. 未解决项
  6. 是否进入下一轮 review
[NOTIFY_TARGETS]:
  - 代码编程群 (-5039283416)
  - 监控群 (-5131273722)
[STOP_CONDITIONS]:
  - 不允许扩 scope
  - 不允许把未验证内容说成完成
  - 如果发现必须超出范围，立即停止并返回 main
  `,
  runTimeoutSeconds: 600
})
```

## 示例 7: Step 5 Test 全量测试

```javascript
sessions_spawn({
  agentId: "test",
  mode: "run",
  model: "openai/gpt-5.4", // Type A
  thinking: "medium",
  task: `
[PIPELINE]: 星链
[STEP]: Step 5
[ROLE]: test
[LEVEL]: L2
[GOAL]: 执行全量测试与关键回归测试
[CONTEXT]: ${代码修复完成}
[INPUT_FILES]:
  - ${constitution_file}
  - ${acceptance_criteria}
  - ${code_result}
[OUTPUT_PATH]: ~/.openclaw/workspace/agents/test/reports/test-${timestamp}.md
[REQUIRED_OUTPUT]:
  1. 结论：PASS / FAIL
  2. 测试总数
  3. 通过数
  4. 失败数
  5. 失败项明细
  6. 堆栈/日志摘要
  7. 是否建议进入交付
  8. 是否进入 TF 路径
[NOTIFY_TARGETS]:
  - 代码测试群 (-5245840611)
  - 监控群 (-5131273722)
[STOP_CONDITIONS]:
  - 只负责测试，不修代码
  - 失败项必须可复现、可定位
  - 不做主观业务判断
  `,
  runTimeoutSeconds: 600
})
```

## 示例 8: Step 5.5 Gemini 诊断

```javascript
sessions_spawn({
  agentId: "gemini",
  mode: "run",
  model: "gemini/gemini-3.1-pro-preview",
  thinking: "high",
  task: `
[PIPELINE]: 星链
[STEP]: Step 5.5
[ROLE]: diagnosis
[LEVEL]: L2
[GOAL]: 基于测试失败日志输出诊断 memo
[CONTEXT]: ${测试失败日志} + ${修复历史}
[INPUT_FILES]:
  - ${test_failure_log}
  - ${fix_history}
  - ${code_diff}
[OUTPUT_PATH]: ~/.openclaw/workspace/agents/gemini/reports/diagnosis-${timestamp}.md
[REQUIRED_OUTPUT]:
  1. 可能根因
  2. 最可能路径
  3. 被忽略的边界
  4. 风险等级
  5. 建议是继续修、回滚、还是重开方案
[NOTIFY_TARGETS]:
  - 织梦群 (-5264626153)
  - 监控群 (-5131273722)
[STOP_CONDITIONS]:
  - Adversarial 视角找根因
  `,
  runTimeoutSeconds: 300
})
```

## 示例 9: Step 5.5 Brainstorming 根因分析

```javascript
sessions_spawn({
  agentId: "brainstorming",
  mode: "run",
  model: "anthropic/claude-opus-4-6",
  thinking: "high",
  task: `
[PIPELINE]: 星链
[STEP]: Step 5.5
[ROLE]: root-cause-analysis
[LEVEL]: L2
[GOAL]: 基于诊断 memo 输出根因树和替代路径
[CONTEXT]: ${Gemini诊断memo}
[INPUT_FILES]:
  - ${diagnosis_memo}
  - ${epoch_history}
[OUTPUT_PATH]: ~/.openclaw/workspace/agents/brainstorming/reports/root-cause-${timestamp}.md
[REQUIRED_OUTPUT]:
  1. 根因树
  2. 替代修复路径
  3. 回滚触发器
  4. 最小恢复路线
  5. 是否建议回到 Step 1.5 / Step 2 / Step 4
[NOTIFY_TARGETS]:
  - 头脑风暴群 (-5231604684)
  - 监控群 (-5131273722)
[STOP_CONDITIONS]:
  - 不直接写代码或跑测试
  `,
  runTimeoutSeconds: 300
})
```

## 示例 10: Step 5.5 OpenAI 回滚仲裁

```javascript
sessions_spawn({
  agentId: "openai",
  mode: "run",
  model: "openai/gpt-5.4",
  thinking: "high",
  task: `
[PIPELINE]: 星链
[STEP]: Step 5.5
[ROLE]: arbitration
[LEVEL]: L2
[GOAL]: 基于诊断和根因分析给出最终回滚决策
[CONTEXT]: ${Gemini诊断} + ${Brainstorming根因分析}
[INPUT_FILES]:
  - ${diagnosis_memo}
  - ${root_cause_analysis}
  - ${rollback_cost_estimate}
[OUTPUT_PATH]: ~/.openclaw/workspace/agents/openai/reports/rollback-decision-${timestamp}.md
[REQUIRED_OUTPUT]:
  1. 结论：CONTINUE_FIX / ROLLBACK / REPLAN
  2. 理由
  3. 下一步唯一指令
  4. 风险说明
[NOTIFY_TARGETS]:
  - openai 群 (-5242027093)
  - 监控群 (-5131273722)
[STOP_CONDITIONS]:
  - 宪法是唯一最高依据
  - 输出唯一结论
  `,
  runTimeoutSeconds: 300
})
```

## 星鉴流水线示例

### Step 2A: Gemini 研究扫描

```javascript
sessions_spawn({
  agentId: "gemini",
  mode: "run",
  model: "gemini/gemini-3.1-pro-preview",
  thinking: "medium", // S级
  task: `
[PIPELINE]: 星鉴
[STEP]: Step 2A
[ROLE]: scan
[LEVEL]: S
[GOAL]: 研究扫描，不直接给最终主方案
[CONTEXT]: ${研究任务描述}
[INPUT_FILES]:
  - 研究材料
  - 背景文档
[OUTPUT_PATH]: ~/.openclaw/workspace/agents/gemini/reports/research-scan-${timestamp}.md
[REQUIRED_OUTPUT]:
  1. 核心问题
  2. 边界
  3. 关键假设
  4. 风险
  5. 路线候选
  6. 需要宪法定稿的项
[NOTIFY_TARGETS]:
  - 织梦群 (-5264626153)
  - 监控群 (-5131273722)
[STOP_CONDITIONS]:
  - 不直接给最终主方案
  `,
  runTimeoutSeconds: 300
})
```

### Step 2B: OpenAI 研究宪法

```javascript
sessions_spawn({
  agentId: "openai",
  mode: "run",
  model: "openai/gpt-5.4",
  thinking: "medium", // S级
  task: `
[PIPELINE]: 星鉴
[STEP]: Step 2B
[ROLE]: constitution
[LEVEL]: S
[GOAL]: 把研究扫描结果收敛成最终研究宪法
[CONTEXT]: ${Gemini研究扫描结果}
[INPUT_FILES]:
  - ${research_scan_file}
[OUTPUT_PATH]: ~/.openclaw/workspace/agents/openai/reports/research-constitution-${timestamp}.md
[REQUIRED_OUTPUT]:
  1. 目标
  2. 非目标
  3. 问题边界
  4. 评价标准
  5. 风险
  6. 默认假设
  7. 红线
[NOTIFY_TARGETS]:
  - openai 群 (-5242027093)
  - 监控群 (-5131273722)
[STOP_CONDITIONS]:
  - 只做规则收敛
  `,
  runTimeoutSeconds: 300
})
```

### Step 3: Claude 主报告

```javascript
sessions_spawn({
  agentId: "claude",
  mode: "run",
  model: "anthropic/claude-opus-4-6",
  thinking: "medium", // S级
  task: `
[PIPELINE]: 星鉴
[STEP]: Step 3
[ROLE]: planning
[LEVEL]: S
[GOAL]: 基于最终研究宪法输出主报告
[CONTEXT]: ${研究宪法摘要}
[INPUT_FILES]:
  - ${research_constitution_file}
  - ${gemini_scan_file}
[OUTPUT_PATH]: ~/.openclaw/workspace/agents/claude/reports/report-${timestamp}.md
[REQUIRED_OUTPUT]:
  1. 核心结论
  2. 推荐路线
  3. 不推荐路线
  4. Phase 0 / 1 / 2
  5. 现在启用什么
  6. 现在不要启用什么
  7. 风险与回滚触发器
  8. 建议下一步
[NOTIFY_TARGETS]:
  - 小克群 (-5101947063)
  - 监控群 (-5131273722)
[STOP_CONDITIONS]:
  - 基于宪法，不偏离
  `,
  runTimeoutSeconds: 600
})
```

## 关键配置说明

### Review Agent 可调用列表

Review agent 需要能够 spawn 以下 agent：
- `gemini` - 用于 adversarial review 和一致性复核
- `claude` - 用于代码审查
- `openai` - 用于仲裁
- `coding` - 用于修复（如果需要）
- `test` - 用于测试（如果需要）
- `brainstorming` - 用于方案设计（如果需要）
- `docs` - 用于文档（如果需要）

### 模型动态切换

Main agent 通过 spawn 参数动态覆盖模型：

```javascript
// Type A 任务
sessions_spawn({
  agentId: "coding",
  model: "anthropic/claude-sonnet-4-6", // 覆盖默认的 gpt
  thinking: "medium",
  // ...
})

// Type B 任务
sessions_spawn({
  agentId: "coding",
  model: "openai/gpt-5.4", // 使用默认
  thinking: "medium",
  // ...
})
```

### Thinking Level 映射

- `low` - 快速预审、简单任务
- `medium` - 常规任务、L2 级别
- `high` - 复杂任务、L3 级别、仲裁

### Timeout 建议

- 扫描/复核：300s (5分钟)
- 宪法/计划：300s (5分钟)
- 开发/修复：600s (10分钟)
- 测试：600s (10分钟)
- 仲裁：300s (5分钟)

## 使用建议

1. **Main agent 作为任务生成器**：Main 根据流水线步骤自动生成标准化的 spawn 任务
2. **模板在 AGENTS.md**：每个 agent 的 AGENTS.md 包含完整的执行模板
3. **任务包装统一**：所有 spawn 都使用相同的结构化格式
4. **通知双链路**：Agent 自推 + Main 补发监控群
5. **结构化输出**：所有产物都有明确的输出结构要求
