# Step 1.5D - Review(Gemini) 一致性复核模板

## 任务类型
星链 Step 1.5D - 一致性复核

## 执行指令

你是反方 reviewer。
请检查 claude 的实施计划是否偏离最终宪法。

## 输出结构
1. 结论：ALIGN / DRIFT / MAJOR_DRIFT
2. 违反宪法的点
3. 漏掉的边界
4. 错误假设
5. 风险遗漏
6. 必改项
7. 可忽略项

## 要求
- 不重写整套计划
- 每条问题都要对应宪法依据
- 重点找遗漏、膨胀、跑偏

## 输入
{{FINAL_CONSTITUTION}}
{{CLAUDE_PLAN}}
