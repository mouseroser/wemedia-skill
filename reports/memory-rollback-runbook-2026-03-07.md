# Memory Rollback Runbook - 2026-03-07

## Purpose
Quickly restore the memory system if the current `memory-lancedb-pro` runtime causes problems.

This runbook assumes the machine is the current main runtime:
- host: `LucifinilCe's M3MacBook Pro`
- config: `/Users/lucifinil_chen/.openclaw/openclaw.json`

## Current Live State
- active runtime memory plugin: `memory-lancedb-pro`
- embeddings: local Ollama + `nomic-embed-text`
- plugin stage: P1
- built-in file memory search is also already repaired separately

## What Can Be Rolled Back
There are two rollback levels:

### Level 1: Roll back plugin config only
Use this if:
- plugin behavior becomes noisy
- `autoCapture` / `autoRecall` causes bad results
- memory plugin loads but behavior is undesirable

Effect:
- keep the plugin files on disk
- revert `openclaw.json` to an earlier state
- restart gateway

### Level 2: Disable plugin and fall back to built-in memory search
Use this if:
- plugin fails to load
- plugin DB is corrupted
- plugin CLI/tools behave unpredictably
- you want the fastest path back to the simpler built-in memory layer

Effect:
- remove `plugins.slots.memory = memory-lancedb-pro`
- disable plugin entry
- restart gateway
- rely on built-in `memory_search` again

## Backup Files Already Created
- `/Users/lucifinil_chen/.openclaw/openclaw.json.memory-fix.bak`
- `/Users/lucifinil_chen/.openclaw/openclaw.json.memory-lancedb-pro.bak`
- `/Users/lucifinil_chen/.openclaw/openclaw.json.plugins-allow.bak`
- `/Users/lucifinil_chen/.openclaw/openclaw.json.autorecall.bak`
- `/Users/lucifinil_chen/.openclaw/openclaw.json.autocapture.bak`

## Recommended Rollback Order

### Option A: Roll back only P1 behavior
If the issue is specifically `autoRecall` / `autoCapture`, restore:
- `/Users/lucifinil_chen/.openclaw/openclaw.json.memory-lancedb-pro.bak`

Why:
- that backup represents the first minimal plugin deployment before later tuning

### Option B: Roll back plugin deployment entirely
If the plugin itself is the issue, restore:
- `/Users/lucifinil_chen/.openclaw/openclaw.json.memory-fix.bak`

Why:
- that backup is from the stage where built-in file memory search had already been repaired, but `memory-lancedb-pro` had not yet been deployed

This is the cleanest fallback target.

## Rollback Commands

### Roll back to built-in memory search only
```bash
cp /Users/lucifinil_chen/.openclaw/openclaw.json.memory-fix.bak \
   /Users/lucifinil_chen/.openclaw/openclaw.json

openclaw doctor
openclaw gateway restart
openclaw status
```

Expected result:
- `memory-lancedb-pro` no longer owns the memory slot
- built-in `memory_search` remains available

### Roll back to first minimal plugin deployment
```bash
cp /Users/lucifinil_chen/.openclaw/openclaw.json.memory-lancedb-pro.bak \
   /Users/lucifinil_chen/.openclaw/openclaw.json

openclaw doctor
openclaw gateway restart
openclaw status
openclaw plugins info memory-lancedb-pro
```

Expected result:
- plugin still loads
- later tuning such as allowlist/autorecall/autocapture changes are removed

## Manual Minimal Disable Path
If backup files are unavailable, do this manually inside `openclaw.json`:
- remove memory-lancedb-pro from `plugins.entries`
- remove it from `plugins.load.paths`
- remove `plugins.slots.memory = "memory-lancedb-pro"`
- keep the repaired built-in `agents.defaults.memorySearch` / `main.memorySearch`

Then run:
```bash
openclaw doctor
openclaw gateway restart
openclaw status
```

## Verify After Rollback
Run these checks:
```bash
openclaw status
openclaw plugins list
openclaw plugins info memory-lancedb-pro
openclaw memory search --query '晨星 Telegram' --json
```

Healthy fallback means:
- gateway starts cleanly
- memory path is available again
- no broken plugin state blocks startup
- basic memory query returns results

## What Not To Delete In A Hurry
Do not rush to delete these paths during rollback:
- `~/.openclaw/workspace/plugins/memory-lancedb-pro`
- `~/.openclaw/workspace/intel/collaboration/memory-lancedb-pro`
- `~/.openclaw/memory/lancedb-pro`

Reason:
- config rollback is reversible and low-risk
- deleting runtime files or DB directories is destructive and unnecessary for first response

## Recommended First Response If Something Feels Off
1. Check `openclaw status`
2. Check `openclaw plugins info memory-lancedb-pro`
3. Run one memory query through CLI
4. If issue is just noisy recall, roll back to minimal plugin deployment
5. If issue is plugin instability, roll back to built-in memory search only
6. Only consider deleting DB/runtime files after config rollback fails

## Practical Rule
Prefer configuration rollback before data deletion.

That gives the fastest path back to a working memory system with the least risk.
