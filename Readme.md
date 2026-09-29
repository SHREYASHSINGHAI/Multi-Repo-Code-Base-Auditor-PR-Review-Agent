> AI-Driven Token-Efficient Codebase Auditor & Automated PR Review Agent

Sentinel-Code is a lightweight, context-aware AI auditing engine designed to catch security vulnerabilities, architectural anti-patterns, and breaking changes before they reach production. Powered by LangChain, Model Context Protocol (MCP), and Gemini 2.5 Flash, it optimizes token consumption by executing smart heuristic diff-filtering prior to LLM analysis.

---

## Key Features

* **Smart Pre-Filtering Engine**: Analyzes AST and diff metadata locally to ignore whitespace, comments, and trivial documentation updates, reducing LLM token consumption by up to 90%+.
* **File-Aware Audit Reports**: Extracts modified file paths directly from Git headers to deliver file-level risk assessments with exact line attributions.
* **Context-Driven Security Enforcement**: Audits code diffs dynamically against custom team/org guidelines defined in `security_rules.md`.
* **Zero-Config Pre-Commit Hooks**: Plugs natively into Git hooks (`.git/hooks/pre-commit`) to block high-risk security flaws locally before commits enter git history.
* **Non-Disruptive Execution**: Built-in AST filters skip non-code modifications in milliseconds with zero LLM API cost.

---

## System Architecture

```text
[ Developer Executing git commit / CLI ]
            │
            ▼
┌───────────────────────┐
│  Git Staged Extractor │
│ (git diff --staged)   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│   Heuristic Filter    │ ◄── Parse file paths & isolate
│ (core/filter.py)      │     meaningful logic changes
└───────────┬───────────┘
            │
┌───────────┴─────────┐
│                     │
(Trivial)       (Meaningful Change)
│                     │
▼                     ▼
[ SKIP AUDIT ]    ┌──────────────────────┐
(0 Tokens Used)   │  Rules & Guidelines  │ (rules/security_rules.md)
                  └──────────┬───────────┘
                             │
                             ▼
                   ┌──────────────────────┐
                   │  CodeAuditorBrain    │ (LangChain + Gemini 2.5 Flash)
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │   Terminal / PR      │
                   │   Structured Report  │
                   └──────────────────────┘
Project Structure
Plaintext
sentinel_code/
├── core/
│   ├── __init__.py
│   ├── auditor_agent.py   # LangChain ReAct Auditor Agent (Gemini 2.5 Flash)
│   ├── filter.py          # Smart heuristic pre-filter & file metadata parser
│   └── rules_loader.py    # Rule loader for security_rules.md
│
├── interfaces/
│   ├── __init__.py
│   └── cli.py             # Terminal interface & Git pre-commit wrapper
│ 
├── rules/
│   └── security_rules.md  # Security and architectural compliance policies
│ 
├── sample_code.py         # Sample test file for vulnerability simulation
│ 
├── requirements.txt       # Project dependencies
│ 
└── README.md


Getting Started
1. Prerequisites
Python 3.10 or higher

Git installed and configured

Google Gemini API Key

2. Environment Setup
Clone the repository and set up a virtual environment:

Bash
git clone [https://github.com/your-username/sentinel-code.git](https://github.com/your-username/sentinel-code.git)
cd sentinel-code

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Set up your Gemini API key in your environment variables:

Bash
# On Linux/macOS
export GOOGLE_API_KEY="your-gemini-api-key"

# On Windows (PowerShell)
$env:GOOGLE_API_KEY="your-gemini-api-key"
Usage & Testing
Running the CLI Directly
Make a change in your project or add a file containing code changes:

Bash
git add sample_code.py
Run the Sentinel-Code local CLI auditor:

Bash
python -m interfaces.cli