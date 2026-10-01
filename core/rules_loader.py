from pathlib import Path

SENTINEL_RULES = Path(__file__).resolve().parent.parent / "rules" / "security_rules.md"
FALLBACK = "Standard Secure Coding Guidelines: Avoid hardcoded secrets, SQL injection, and unhandled exceptions."

def load_security_rules(rules_path: str = "rules/security_rules.md") -> str:

    for path in (Path(rules_path), SENTINEL_RULES):
        if path.exists():
            return path.read_text(encoding="utf-8").strip()
    return FALLBACK