# MEMORY.md - Gemini Agent

## 血泪教训
- Gemini 曾出现“completed 但无输出”的假完成现象；必须以文件落盘或实际产物为准，不能只信状态。
- Gemini / OpenAI-compatible 兼容层曾因 `tools[0].function_declarations[*].name: Invalid function name` 在生成前被 provider 400 拒绝；表面看像空输出，实质是工具 schema 兼容性问题。
- 不要把扫描模板、流程步骤、输出格式定义混进 MEMORY.md；这些属于 `AGENTS.md`。

## 错误示范 / 反模式
- 看到 status=done 就默认任务成功。
- 把扫描稿直接当最终方案，不做一致性复核。
- 用 MEMORY.md 存放流程模板或固定输出结构。

## 长期稳定规则
- Gemini 的关键任务以“实际文件 / 实际输出存在”为完成标准。
- 带工具的复杂任务如再复现兼容性问题，应及时切换 Claude / OpenAI fallback。
- Gemini 更适合扫描、对齐、复核；不负责最终拍板。
