# Learnings

Append structured entries:
- LRN-YYYYMMDD-XXX for corrections / best practices / knowledge gaps
- Include summary, details, suggested action, metadata, and status


## [LRN-20260308-001] best_practice

**Logged**: 2026-03-08T03:07:34.594Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
launchd plist for local services should use the actual user-installed `uv` path, not assume `/opt/homebrew/bin/uv`

### Details
While installing the local rerank sidecar as a macOS LaunchAgent, the first plist used `/opt/homebrew/bin/uv` and failed with launchd exit code EX_CONFIG. On this machine the real binary is `/Users/lucifinil_chen/.local/bin/uv`. After correcting the ProgramArguments path, the service loaded and served health checks normally.

### Suggested Action
When generating launchd plists for uv-managed services, resolve `which uv` first and template the absolute path into the plist.

### Metadata
- Source: memory-lancedb-pro/self_improvement_log
---
