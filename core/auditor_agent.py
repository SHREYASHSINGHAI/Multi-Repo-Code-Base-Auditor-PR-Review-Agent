import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from core.filter import is_meaningful_change
from core.rules_loader import load_security_rules

class CodeAuditorBrain:
    def __init__(self, model_name: str = "Gemini 3.8 Flash"):
        # Initialize LLM (Gemini 2.5 Flash is super fast and cheap for hackathons)
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.1  # Low temperature for strict auditing
        )
        self.rules = load_security_rules()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Sentinel-Code, an expert Senior Security & Architecture Auditor.
Your job is to analyze code diffs against strict Security and Architecture Rules.

### Security Rules & Guidelines:
{rules}

### Output Instructions:
1. If NO security or architecture violations are found, return:
   "✅ **Audit Passed**: Code is safe and compliant with rules."
2. If violations are found, return a structured markdown response:
   - **Risk Level**: [HIGH / MEDIUM / LOW]
   - **Violation Summary**: Concise summary of what rule was broken.
   - **Affected Line / Code**: Excerpt from diff.
   - **Suggested Fix**: Corrected code block.

Keep responses concise, direct, and actionable."""),
            ("user", "Analyze this code diff:\n\n```diff\n{diff}\n```")
        ])

        self.chain = self.prompt | self.llm

    async def run_audit(self, diff_text: str) -> str:
        """Runs the smart audit pipeline."""
        # 1. Smart Heuristic Pre-Filter Check
        if not is_meaningful_change(diff_text):
            return "⚡ **[Audit Skipped]**: Only trivial formatting or comment changes detected. 0 tokens used."

        # 2. Truncate diff if oversized to control token spending
        max_chars = 6000
        if len(diff_text) > max_chars:
            diff_text = diff_text[:max_chars] + "\n... [Diff truncated for token budget]"

        # 3. Invoke Agent Chain
        response = await self.chain.ainvoke({
            "rules": self.rules,
            "diff": diff_text
        })

        return response.content