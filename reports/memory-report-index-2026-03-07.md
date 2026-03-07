# Memory Report Index - 2026-03-07

## Purpose
This index links the key memory-system documents produced during the 2026-03-07 rollout, so future review does not require replaying the full chat history.

## Recommended Reading Order
1. `reports/memory-rollout-changelog-2026-03-07.md`
   - Fastest high-level timeline of what changed
   - Best starting point for a quick recap

2. `reports/memory-system-status-2026-03-07.md`
   - Current live state snapshot
   - Includes active config, paths, backups, known boundaries, and practical conclusion

3. `reports/memory-observation-checklist-2026-03-07.md`
   - What to watch during normal use
   - Defines what counts as a real recall miss and when to add atomic memory

4. `reports/memory-rollback-runbook-2026-03-07.md`
   - Recovery guide if the current memory plugin runtime becomes noisy or unstable
   - Includes two rollback levels and ready-to-run commands

## Document Roles
- `reports/memory-rollout-changelog-2026-03-07.md`
  - Chronological change summary
  - Best for answering: "What happened tonight?"

- `reports/memory-system-status-2026-03-07.md`
  - Configuration and runtime snapshot
  - Best for answering: "What is running right now?"

- `reports/memory-observation-checklist-2026-03-07.md`
  - Post-rollout operating guidance
  - Best for answering: "When should we tune more?"

- `reports/memory-rollback-runbook-2026-03-07.md`
  - Failure recovery path
  - Best for answering: "How do we get back to safety quickly?"

## One-Line Current Conclusion
As of 2026-03-07, the memory system has moved from repair mode to stable observation mode:
- built-in file memory search is repaired
- `memory-lancedb-pro` is live as the runtime memory plugin
- P1 is enabled (`autoRecall` + `autoCapture`)
- historical memory has been imported
- high-frequency chat recall has been stabilized with atomic memories
- future changes should be driven by real misses, not blind tuning
