# 2026-03-08 No-Loss Recovery Manifest

## Goal
- Preserve all recoverable work from 2026-03-08, especially the v2.5 architecture work, template work, and the previously deleted agent/template directories.

## Recovered Architecture Outputs
- `AGENTS.md` — restored
- `MEMORY.md` — restored
- `agents/openai/AGENTS.md` — restored
- `agents/openai/SOUL.md` — restored
- `agents/review/AGENTS.md` — restored
- `agents/claude/SOUL.md` — restored
- `agents/gemini/SOUL.md` — restored
- `intel/starchain-templates/spawn-task-format.md` — restored
- `intel/starchain-templates/step-1.5A-gemini-scan.md` — restored
- `intel/starchain-templates/step-1.5B-openai-constitution.md` — restored
- `intel/starchain-templates/step-1.5C-claude-plan.md` — restored
- `intel/starchain-templates/step-1.5D-review-gemini.md` — restored
- `intel/starchain-templates/step-1.5E-review-openai.md` — restored

## Existing Upstream Evidence
- `/Users/lucifinil_chen/.openclaw/skills/starchain/references/pipeline-v2-5-contract.md`
- `/Users/lucifinil_chen/.openclaw/skills/starchain/references/PIPELINE_FLOWCHART_V2_5_EMOJI.md`
- `/Users/lucifinil_chen/.openclaw/skills/starchain/references/STARCHAIN_V2_5_SUMMARY.md`
- `/Users/lucifinil_chen/.openclaw/skills/starchain/references/arbitration-rubric.md`
- `/Users/lucifinil_chen/.openclaw/skills/starchain/references/arbitration-trigger-conditions.md`
- `/Users/lucifinil_chen/.openclaw/memory/backups/memory-backup-2026-03-08.jsonl`
- `/Users/lucifinil_chen/.openclaw/agents/main/sessions/d4bb1fb4-fea8-4bf4-8829-0c01124dab0a.jsonl.reset.2026-03-08T10-24-10.873Z`

## Raw Recovery Sources
- Exact or longest recovered tool payloads from the session are archived in `reports/recovery-2026-03-08-no-loss/raw-extracted/`.
- Current restored files are snapshotted in `reports/recovery-2026-03-08-no-loss/snapshot/`.

## Known Temporary Artifact
- `memory/2026-03-08-step4-templates.md` was previously deleted, but its existence is evidenced in `~/.openclaw/logs/gateway.log`; the substantive template content has been preserved in `intel/starchain-templates/` and the raw session extracts.

## Functional Work Preserved
- Local rerank sidecar work remains present in `services/local-rerank-sidecar/` and related scripts under `scripts/`.
- Recent commits still present: `0c6a424`, `d87180f`, `d85c7c5`, `3a7abcd`.