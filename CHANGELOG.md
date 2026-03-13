# Changelog

## 2026-03-13

### Changed
- Adopted **main-first** notification reliability for the WeMedia pipeline.
- Clarified that child-agent Telegram messages are **best-effort** only.
- Required `main` to guarantee visibility for key progress, results, failures, and alerts.

### Rationale
- Real-world verification showed that `sessions_spawn(mode=run)` subagents can complete and announce successfully while their own `message(...)` calls may still fail to deliver.
- To keep the pipeline observable and predictable, reliable notifications must be centralized in `main`.
