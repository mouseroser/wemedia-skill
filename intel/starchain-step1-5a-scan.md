# NotebookLM 提取整理 → 保存到笔记 - 需求扫描报告

作为 Gemini（织梦），针对 Step 1.5A 的任务“实现 NotebookLM 提取整理 → 保存到笔记”进行了扫描，以下是识别出的歧义、边界、风险和技术隐患：

## 1. 发现的问题与需求歧义
* **“提取”的定义不明确**：是从外部信息源（如网页、本地文件、聊天记录）中提取内容？还是指从 NotebookLM 中通过 query / artifact 提取生成的总结？
* **“整理”的逻辑不明确**：是由 LLM 进行降噪、摘要和结构化处理（例如转为 Markdown），还是仅原样保留？
* **“保存到笔记”的具体形式**：目标如果是 NotebookLM，是指保存为其中的一个 `Note`（独立笔记）还是 `Source`（文档源）？目标如果是本地，是指怎样的文件系统结构？

## 2. 边界问题
* **目标 Notebook**：如果保存到 NotebookLM，是特定的 notebook（如 `memory`、`media-research`），还是动态指定的？
* **笔记格式与标题规则**：落盘的笔记格式是什么？如何命名？是否统一采用诸如 `[归档] YYYY-MM-DD-主题.md` 的规范？
* **容量限制**：NotebookLM 的单个 Notebook 有 50 个 Source 的额度上限，以及单文件 100KB/500,000 words 的限制，高频或大批量的归档可能会很快耗尽配额。

## 3. 技术风险与隐患
* **`nlm-gateway.sh` 写入能力缺失**：经过查阅当前网关脚本，发现 **支持 `source add` 导入本地文件为文档源**，以及 `note convert-to-source`。但是，**并没有直接提供创建/保存为 NotebookLM Note（笔记）的 API (`note add` 或 `note create`)**。如果强行要保存在 NotebookLM 里，必须采用先在本地生成 `.md` 文件，再作为 Source 导入的方式。
* **网络与 RPC 不稳定性**：在测试调用 `nlm-gateway.sh query` 时遇到了底层 `RPC GET_LAST_CONVERSATION_ID failed` 等错误。证明强依赖代理和无头浏览器协议的命令在自动化流水线中容易因网络或状态超时而失败。
* **锁竞争 (`nlm.lock`)**：现有的网关脚本在进行添加/修改等写操作时会使用单例锁，并发提取可能导致超时甚至丢失数据。

## 4. 方案可行性建议
基于当前的脚本能力，如果任务的终点是 NotebookLM 内部，**直接通过 API 创建 Note 是不可行的**。建议的数据流方案如下：
1. **统一提取与整理**：由 `gemini` 负责调用轻量级模型对目标内容进行摘要、格式化处理。
2. **强制本地落盘**：整理后的内容必须首先保存在本地指定的归档目录下（如 `~/.openclaw/workspace/notes/`），以此为唯一事实来源，避免直接写入 NotebookLM 失败导致数据丢失。
3. **异步/离线入库**：如果必须存入 NotebookLM，通过执行 `nlm-gateway.sh source add` 将本地 Markdown 文件作为 Source（而不是 Note）导入指定的 Notebook 中。如果失败，则仅记录告警。

## 5. 待明确的问题（需向 Main/晨星 确认）
1. **数据流向**：是指“提取外部信息 -> 整理 -> 存入 NotebookLM”，还是“从 NotebookLM 提取总结 -> 整理 -> 存入本地文件”？
2. **存在形态**：由于目前底层接口限制，如果以“源（Source）”的形式存入 NotebookLM，是否可以接受（作为 Note 的替代）？
3. **目标位置**：存入哪个具体的 Notebook 或者本地哪个具体的文件夹？