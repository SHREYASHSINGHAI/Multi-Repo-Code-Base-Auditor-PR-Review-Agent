"""
Sentinel-Code benchmark: replay real commits through the pre-filter.

Usage (run from the Sentinel-Code repo root, or pass --sentinel):
    python benchmark.py --repo /path/to/any/git/repo --n 50
    python benchmark.py --repo . --n 50 --csv results_self.csv

What it measures (no API key needed, costs nothing):
  - skip rate: share of commits the filter would NOT send to the LLM
  - estimated tokens: baseline (send every diff) vs filtered (send only kept diffs)
  - filter latency per commit
"""
import argparse
import csv
import statistics
import subprocess
import sys
import time
from pathlib import Path

CHARS_PER_TOKEN = 4          
MAX_DIFF_CHARS = 6000      


def run(cmd, cwd):
    return subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=60,
    ).stdout


def list_commits(repo, n):
    out = run(["git", "log", "--no-merges", f"-n{n}", "--format=%H"], repo)
    return [line for line in out.splitlines() if line.strip()]


def commit_diff(repo, sha):
    # --format= suppresses the commit header so we get only the diff
    return run(["git", "show", "--format=", sha], repo)


def est_tokens(chars):
    return chars // CHARS_PER_TOKEN


def save_results_to_docs(sentinel_path, repo, total, kept, base, filt, trunc, times, rows):
    """Saves the benchmark summary output to docs/assets/filter_test_result.md."""
    assets_dir = Path(sentinel_path) / "docs" / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    file_path = assets_dir / "filter_test_result.md"

    skip_rate = ((total - kept) / total) * 100 if total else 0
    token_reduction = (1 - filt / base) * 100 if base else 0
    median_latency = statistics.median(times) if times else 0
    max_latency = max(times) if times else 0

    lines = [
        "# Sentinel-Code Pre-Filter Benchmark Results\n",
        f"- **Repo:** `{repo}`",
        f"- **Commits tested:** {total}",
        f"- **Skipped (0 tok):** {total - kept} ({skip_rate:.0f}%)",
        f"- **Sent to LLM:** {kept}",
        f"- **Est. tokens:** baseline {base:,} -> filtered {filt:,}",
        f"- **Token reduction:** {token_reduction:.0f}% (estimated)",
        f"- **Truncated diffs:** {trunc} (> {MAX_DIFF_CHARS} chars, tail NOT audited)",
        f"- **Filter latency:** median {median_latency:.2f} ms, max {max_latency:.2f} ms\n",
        "## Kept Commits (Sent to LLM)\n",
    ]

    for r in rows:
        if r["kept"]:
            lines.append(f"- `{r['sha']}` | {r['diff_chars']:>6} chars | `{r['file_list']}`")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\nBenchmark results saved to {file_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", help="git repo whose history to replay")
    ap.add_argument("--sentinel", default=".", help="path to Sentinel-Code repo root")
    ap.add_argument("--n", type=int, default=50, help="number of recent commits")
    ap.add_argument("--overhead-tokens", type=int, default=400,
                    help="estimated system prompt + rules tokens added to every LLM call")
    ap.add_argument("--csv", default=None, help="write per-commit results to this file")
    args = ap.parse_args()

    sys.path.insert(0, str(Path(args.sentinel).resolve()))
    from core.filter import parse_diff_metadata  # your real filter

    repo = str(Path(args.repo).resolve())
    shas = list_commits(repo, args.n)
    if not shas:
        sys.exit("No commits found.")

    rows, times = [], []
    for sha in shas:
        diff = commit_diff(repo, sha)
        if not diff.strip():
            continue
        t0 = time.perf_counter()
        files, meaningful = parse_diff_metadata(diff)
        times.append((time.perf_counter() - t0) * 1000)

        sent_chars = min(len(diff), MAX_DIFF_CHARS)
        tokens = est_tokens(sent_chars) + args.overhead_tokens
        rows.append({
            "sha": sha[:8],
            "files": len(files),
            "diff_chars": len(diff),
            "kept": meaningful,
            "baseline_tokens": tokens,
            "filtered_tokens": tokens if meaningful else 0,
            "truncated": len(diff) > MAX_DIFF_CHARS,
            "file_list": ";".join(files)[:120],
        })

    total = len(rows)
    kept = sum(r["kept"] for r in rows)
    base = sum(r["baseline_tokens"] for r in rows)
    filt = sum(r["filtered_tokens"] for r in rows)
    trunc = sum(r["truncated"] for r in rows)

    print(f"\nRepo:            {repo}")
    print(f"Commits tested:  {total}")
    print(f"Skipped (0 tok): {total - kept}  ({(total - kept) / total:.0%})")
    print(f"Sent to LLM:     {kept}")
    print(f"Est. tokens:     baseline {base:,}  ->  filtered {filt:,}")
    print(f"Token reduction: {(1 - filt / base):.0%}  (estimated)")
    print(f"Truncated diffs: {trunc}  (> {MAX_DIFF_CHARS} chars, tail NOT audited)")
    print(f"Filter latency:  median {statistics.median(times):.2f} ms, max {max(times):.2f} ms")

    print("\nKept commits (check these by eye - are they really logic changes?):")
    for r in rows:
        if r["kept"]:
            print(f"  {r['sha']}  {r['diff_chars']:>6} chars  {r['file_list']}")

    # Save summary report to docs/assets/filter_test_result.md
    save_results_to_docs(args.sentinel, repo, total, kept, base, filt, trunc, times, rows)

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)
        print(f"\nPer-commit results written to {args.csv}")


if __name__ == "__main__":
    main()