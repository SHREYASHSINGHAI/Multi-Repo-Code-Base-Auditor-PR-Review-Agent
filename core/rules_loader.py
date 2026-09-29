import os

def load_security_rules(rules_path: str = "rules/security_rules.md") -> str:

    if not os.path.exists(rules_path):
        return "Standard Secure Coding Guidelines: Avoid hardcoded secrets, SQL injection, and unhandled exceptions."
    
    with open(rules_path, "r", encoding="utf-8") as f:
        return f.read().strip()