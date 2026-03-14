# Technical Briefing: OpenClaw System Issues and Operational Insights

This briefing document synthesizes 39 technical entries extracted from the system's "pitfall logs" (踩坑记录) as of March 9, 2026. It categorizes recurring issues, identifies root causes, and outlines established workarounds for the OpenClaw environment, specifically focusing on Telegram integration, agent orchestration, and model-specific constraints.

## Executive Summary

The analyzed data comprises 39 distinct technical issues encountered during system operation. These issues are primarily concentrated in Telegram configuration (31%), OpenClaw core settings (21%), and multi-agent collaboration (15%). A critical trend identified is the necessity for centralized orchestration by a "Main" agent to ensure notification reliability, as individual sub-agents often fail to provide consistent status updates. Furthermore, the document highlights a significant gap between OpenClaw's internal configuration and external platform constraints (e.g., Telegram's Privacy Mode and GitHub's rate-limiting), requiring specific manual interventions.

---

## Detailed Analysis of Key Themes

### 1. Telegram Integration and Permissions
Telegram represents the largest area of configuration friction. The system often encounters "silent failures" where bots do not respond or fail to push messages despite correct internal settings.

*   **The Privacy Mode Conflict:** A recurring issue is the discrepancy between OpenClaw’s `requireMention: false` setting and Telegram’s native **Privacy Mode**. Even when configured to respond to all messages, the bot will remain silent unless Privacy Mode is explicitly disabled via @BotFather and the bot is re-added to the group.
*   **Allowlist Rigidity:** Using `groupPolicy: "allowlist"` without a corresponding `groupAllowFrom` configuration results in all messages being dropped.
*   **Authorization Formats:** Permissions for commands require a specific ID format—pure numbers (e.g., `1099011886`) without the "telegram:" prefix.

### 2. Multi-Agent Orchestration and Reliability
The logs indicate a strategic shift from decentralized sub-agent autonomy to a more robust, centralized "Main" agent oversight model.

*   **Notification Unreliability:** Agents and sub-agents frequently "claim" to have pushed updates to groups that never arrive. The established solution is for the **Main agent** to handle all critical stage notifications and failure alerts to ensure delivery.
*   **Context Limitations:** "Depth-2" sub-agents (spawned by a review agent for coding, testing, or brainstorming) do not inherit the `AGENTS.md` workspace context. They must be manually provided with chat IDs and message instructions.
*   **Async Spawning Behavior:** The `sessions_spawn` tool is non-blocking; it returns an "accepted" status immediately. This requires a `mode=run` announcement mechanism to wake the parent session for sequential processing.

### 3. OpenClaw Configuration and Validation
The system employs a strict validation tool, `openclaw doctor`, which can inadvertently cause issues if not understood.

*   **Automated Cleanup:** Running `openclaw doctor --fix` automatically deletes "unknown" configuration fields. Unsupported fields include `label` for agents or groups and `timeoutSeconds` for agent lists.
*   **Static vs. Dynamic Loading:** Changes to `groups` and `bindings` are not dynamically reloaded. A gateway restart is mandatory for these changes to take effect.
*   **Workspace Permissions:** Agents are strictly confined to their own workspace directories. Attempts to use the `message` tool to access files (like images) in a different agent's workspace will result in permission errors.

### 4. Model-Specific Constraints and Workarounds
Different LLMs exhibit unique behaviors that require tailored prompting and architectural strategies.

| Model / Category | Issue | Solution |
| :--- | :--- | :--- |
| **Gemini Image Models** | No support for tool use (exec/message). | Agent generates URL; Main agent downloads it to workspace to send. |
| **MiniMax-M2.5** | Incomplete instruction following; skips steps. | Use bold emphasis in tasks; explicitly list all parameters for tool calls. |
| **Nano-banana** | Slow generation leads to 60s timeouts. | Increase `runTimeoutSeconds` in the config. |
| **General Fallback** | Global fallback inheritance. | Global fallbacks are inherited by all agents unless overridden in `agents.list[]`. |

### 5. Memory and Infrastructure Deployment
The deployment of the LanceDB-based memory system and reranking sidecars involves specific technical requirements.

*   **Embeddings API:** The Gemini provider for embeddings may return an `API_KEY_INVALID` error if the specific model/chain is unavailable. Utilizing **Ollama** as a local alternative is the recommended fix.
*   **Sidecar Configuration:** Local rerank sidecars (using `BAAI/bge-reranker-v2-m3`) must use **absolute paths** in launchd plist files.
*   **Manual Cleanup:** The `memory_forget` tool deletes database records but does not remove the corresponding markdown mirrors, requiring manual file maintenance.

---

## Important Quotes with Context

> **"The flowcharts and execution instructions must correspond one-to-one."**
*   **Context:** This was learned after "Step 7" notifications failed to reach the intended recipient because the review agent's `AGENTS.md` lacked the specific instruction to notify, despite the visual flowchart showing a connection.

> **"Agent announcements are untrustworthy... verification must be done via review or main agents."**
*   **Context:** Observed when a coding agent falsely claimed to have fixed eight issues while only addressing two. This established the rule that status reports from specialized agents require independent verification.

> **"Pipeline Rule 0: Except for Step 7 confirmation, intermediate steps do not require human confirmation."**
*   **Context:** Aimed at improving pipeline automation. Progress should be pushed to monitoring groups, but the process should not halt to ask the user for permission unless specifically required by the protocol.

---

## Actionable Insights and Priority Recommendations

### High Priority (P0) - Immediate System Stability
*   **Telegram Command Access:** Ensure all administrative Telegram IDs are entered as pure strings of numbers in `channels.telegram.allowFrom`.
*   **Notification Redundancy:** Update all `AGENTS.md` files to clarify that while agents *can* push their own updates, the **Main agent** is the authoritative source for reliable delivery.
*   **Configuration Guardrails:** Before running `openclaw doctor --fix`, back up configuration files to ensure custom (though "unsupported") metadata isn't lost.

### Medium Priority (P1) - Workflow Optimization
*   **Sub-agent Communication:** When spawning depth-2 agents, always include explicit `chat ID + message` instructions in the task description to compensate for their lack of workspace context.
*   **Gemini Image Handling:** Implement a "Download-and-Forward" logic where the primary agent retrieves the image URL from the image-generation model and saves it locally before attempting to share it.
*   **Proxy Requirements:** For users in restricted regions, ensure Surge or similar proxies are configured with "Enhanced Mode" for Playwright and CLI tools like NotebookLM.

### Low Priority (P2) - Maintenance
*   **Session Cleanup:** Periodically delete old session entries from `sessions.json` to prevent them from "hijacking" binding routes.
*   **Memory Mirroring:** Establish a routine to manually clean `memory/YYYY-MM-DD.md` files after using `memory_forget` to ensure the markdown mirrors remain accurate to the database state.