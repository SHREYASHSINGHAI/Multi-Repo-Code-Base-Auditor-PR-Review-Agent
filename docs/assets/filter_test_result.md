# Sentinel-Code Pre-Filter Benchmark Results

- **Repo:** `D:\Multi-Repo Code Base Auditor & PR Review Agent`
- **Commits tested:** 29
- **Skipped (0 tok):** 16 (55%)
- **Sent to LLM:** 13
- **Est. tokens:** baseline 20,781 -> filtered 10,848
- **Token reduction:** 48% (estimated)
- **Truncated diffs:** 1 (> 6000 chars, tail NOT audited)
- **Filter latency:** median 0.19 ms, max 2.43 ms

## Kept Commits (Sent to LLM)

- `66705a2e` |   2274 chars | `core/auditor_agent.py`
- `e22bb95c` |   7985 chars | `core/filter.py`
- `b8473347` |    183 chars | `.env`
- `30eb8cab` |    559 chars | `core/auditor_agent.py`
- `ac34ae23` |    836 chars | `.gitignore;core/auditor_agent.py`
- `2504bd9b` |   1365 chars | `interfaces/cli.py`
- `8e6f75e6` |   2155 chars | `core/auditor_agent.py`
- `e9428c05` |    682 chars | `sample_code.py;test_brain.py`
- `dc57718b` |    767 chars | `test_brain.py`
- `943abbf0` |   1458 chars | `core/filter.py`
- `95cefff1` |   3372 chars | `core/auditor_agent.py`
- `faa17bd4` |   2430 chars | `core/auditor_agent.py`
- `30a632a7` |    533 chars | `core/rules_loader.py`
