# memory-lancedb-pro Research Constitution (Xingjian Step 2)

## 1. Problem Definition (问题定义)

The `memory-lancedb-pro` project is a memory plugin designed for OpenClaw. It extends the built-in `memory-lancedb` plugin by introducing a robust hybrid retrieval system (Vector + BM25) and cross-encoder reranking. Our objective is to evaluate its suitability for integration into our OpenClaw system while maintaining our established local file memory (`MEMORY.md` + `memory/YYYY-MM-DD.md`) as the primary truth layer. The goal is to leverage its advanced retrieval capabilities without replacing our existing core memory architecture.

## 2. Boundaries & Scope (边界与范围)

**What it should do:**
- Serve as a high-performance secondary retrieval index for specific memory components (e.g., fast vector search, BM25 keyword matching).
- Utilize its advanced multi-stage scoring pipeline (recency boost, time decay, importance weight, length normalization) to surface relevant historical contexts.
- Provide a robust toolset for agents to store, recall, update, and forget isolated memory snippets across multiple scopes (e.g., global, agent-specific).
- Offer multi-scope isolation to segregate knowledge when needed.

**What it should NOT do:**
- It **must not** replace the local file memory (`MEMORY.md` + `memory/YYYY-MM-DD.md`) as the ultimate source of truth. The local markdown files remain the authoritative, human-readable record.
- It should not dictate the primary session strategy unless explicitly configured (e.g., using `mdMirror` as a supplementary function, not a replacement for our existing text-based memory files).

## 3. Embedding Compatibility (嵌入支持)

The plugin abstracts embeddings through its `src/embedder.ts` component, supporting any OpenAI-compatible API. This explicitly covers our target models:

- **Gemini Support:** Full support via the Google Generative AI endpoint configured as an OpenAI-compatible URL (`https://generativelanguage.googleapis.com/v1beta/openai/`).
- **Ollama Support:** Full support for local models (e.g., `nomic-embed-text`) via the local Ollama API endpoint (`http://localhost:11434/v1`). The configuration allows matching dimensions to the specific local model output.
- **Other Providers:** Supports Jina, OpenAI, etc.

## 4. Assumptions (假设)

- We assume the Gateway service process will correctly inherit necessary environment variables (e.g., API keys) if configured using `${...}` syntax.
- We assume the multi-stage scoring parameters (weights, half-lives) can be tuned to prevent historical noise from overwhelming recent, critical context.
- We assume the markdown mirror (`mdMirror`) feature or our own existing file operations can coexist without creating infinite loops or data corruption.

## 5. Risks (风险)

1.  **Context Pollution:** Unfiltered auto-capture or aggressive auto-recall might inject excessive or irrelevant information into the agent's prompt context, leading to hallucinations or token limit exhaustion.
2.  **State Desync:** If LanceDB storage and our local `MEMORY.md`/daily files fall out of sync, the agent might retrieve conflicting information from the different layers.
3.  **Complexity Overhead:** The multi-stage retrieval pipeline (BM25, vector, cross-encoder rerank) introduces additional API dependencies (if using external rerankers) and configuration complexity, potentially leading to hard-to-debug retrieval failures or timeouts.
4.  **Implicit Behaviors:** Features like `selfImprovement` hooks or `autoRecall` might trigger unintended background actions if not explicitly managed or disabled via configuration.

## 6. Recommended Route (推荐路线)

1.  **Integration Approach:** Deploy `memory-lancedb-pro` strictly as an auxiliary retrieval mechanism. Do not remove or alter the existing `MEMORY.md` and `memory/YYYY-MM-DD.md` infrastructure.
2.  **Configuration Restrictions:**
    - Disable `autoRecall` initially to prevent uncontrolled context injection (`"autoRecall": false`). Require agents to explicitly use `memory_recall` tools.
    - Carefully evaluate and likely disable `mdMirror` if it conflicts with our established local file memory structures, relying on our own file management for the truth layer.
    - Set `sessionStrategy: "systemSessionMemory"` (the default) to maintain OpenClaw's built-in session handling unless the specific plugin reflection hooks are strictly necessary.
3.  **Embedding Setup:** Configure embedding endpoints for Ollama (local dev/fallback) and Gemini (primary), ensuring dimensions are correctly specified in the plugin config.
4.  **Testing Phase:** Conduct a controlled pilot to test the hybrid retrieval efficacy and monitor for state desynchronization between LanceDB and local markdown files.