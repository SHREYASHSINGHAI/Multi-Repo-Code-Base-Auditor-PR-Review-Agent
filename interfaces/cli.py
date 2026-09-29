import asyncio
import subprocess
import sys
from core.auditor_agent import CodeAuditorBrain

def get_staged_git_diff() -> str:
    """Executes 'git diff --staged' to get staged local code changes."""
    try:
        result = subprocess.run(
            ["git", "diff", "--staged"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error getting git diff: {e}")
        return ""
    except FileNotFoundError:
        print("❌ Git is not installed or not found in PATH.")
        return ""

async def main():
    print("🔍 Fetching staged changes from Git...")
    diff_text = get_staged_git_diff()

    if not diff_text:
        print("ℹ️ No staged changes found. Use 'git add <file>' before running audit.")
        sys.exit(0)

    print("🤖 Running Sentinel-Code Local Audit...\n")
    brain = CodeAuditorBrain(model_name="gemini-2.5-flash")
    report = await brain.run_audit(diff_text)
    
    print("=" * 60)
    print(report)
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())