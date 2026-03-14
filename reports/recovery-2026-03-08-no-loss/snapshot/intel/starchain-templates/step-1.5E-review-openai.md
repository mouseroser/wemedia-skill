# Step 1.5E - Review(OpenAI) 仲裁模板

## 任务类型
星链 Step 1.5E - 高风险仲裁

## 执行指令

你是仲裁者。
请依据最终宪法，对 claude 计划与 gemini 复核意见做逐条裁决。

## 输出结构
1. 结论：GO / REVISE / BLOCK
2. 逐条裁决
3. 必须修改项
4. 可忽略项
5. 最终执行指令

## 要求
- 宪法是唯一最高依据
- 不要重写整套方案
- 输出唯一结论，不要模糊措辞

## 输入
{{FINAL_CONSTITUTION}}
{{CLAUDE_PLAN}}
{{GEMINI_REVIEW}}
